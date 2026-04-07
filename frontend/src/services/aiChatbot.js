import { isOnline } from './sync.js'
import { getFAQEntries } from './offlineData.js'
import db from './db.js'
import api from './api.js'

/**
 * AI-Powered Chatbot Service for TechnoPath
 * 
 * Priority chain:
 * 1. Flask chatbot API (if configured and online)
 * 2. OpenAI API (if key configured and online)
 * 3. Rule-based fallback (always works offline)
 * 
 * Maintains conversation history and campus context.
 */

const FLASK_CHATBOT_URL = import.meta.env.VITE_FLASK_CHATBOT_URL || 'http://localhost:5000'
const OPENAI_API_KEY = import.meta.env.VITE_OPENAI_API_KEY || ''
const OPENAI_API_URL = 'https://api.openai.com/v1/chat/completions'
const USE_AI_OFFLINE = false // Set to true to queue AI requests when offline

// Campus context for AI
const CAMPUS_CONTEXT = `
You are the SEAIT Campus Assistant for TechnoPath, a campus guide app for South East Asian Institute of Technology (SEAIT) in Tupi, South Cotabato, Philippines.

CAMPUS INFORMATION:
- MST Building (Main Science and Technology): 4 floors, center of campus. Houses MST 101-120 (1F), MST 201-221 (2F), Computer Labs CL1-CL10 (3F), MST 301-420 (4F)
- JST Building (Junior Science and Technology): 4 floors at back of campus. JST101-102 (1F), JST201-202 labs (2F), seminar rooms (3F)
- RST Building (Research Science and Technology): 3 floors, left-bottom from main gate. Registrar & Accounting (1F), Guidance/Safety/HR/SSC/Student Affairs (2F), IT/Silakbo/Laboratory offices (3F)
- Library: 2 floors, ground floor left wing. Open Mon-Fri 8AM-6PM, Sat 8AM-12PM
- Cafeteria: Center grounds between MST and Gymnasium. Open 7AM-6PM daily
- Gymnasium: Back of campus with basketball/volleyball courts, fitness equipment
- Computer Labs CL1-CL6: All on 3rd floor of MST Building
- Registrar Office: 1st floor RST Building, 7 windows, Mon-Fri 8AM-5PM
- CICT Office: 2nd floor MST Building, near computer labs
- Comfort rooms available on every floor of all buildings, near stairwells

KEY SERVICES:
- Interactive campus map with floor plans
- QR code scanning for room/building info
- Turn-by-turn navigation between locations
- Offline mode works without internet

Be helpful, concise, and friendly. Guide users to use the Navigate tab for directions and Map tab for visual exploration. If unsure, direct them to the Registrar office for official inquiries.
`

// Conversation history (in-memory, per session)
const conversationHistory = []
const MAX_HISTORY = 10

/**
 * Initialize chat history from IndexedDB (for logged-in users)
 */
export async function initChatHistory() {
  if (!isOnline()) return
  try {
    const history = await db.ai_chat_logs.limit(MAX_HISTORY).toArray()
    conversationHistory.push(...history.map(h => ({
      role: h.mode === 'user' ? 'user' : 'assistant',
      content: h.message
    })))
  } catch {
    // Silent fail - start fresh
  }
}

/**
 * Save chat message to local history
 */
async function saveToHistory(mode, message) {
  try {
    await db.ai_chat_logs.add({
      mode,
      message,
      created_at: new Date().toISOString()
    })
  } catch {
    // Silent fail
  }
}

/**
 * Generate response using Flask Chatbot API
 */
async function generateFlaskResponse(userMessage) {
  const response = await fetch(`${FLASK_CHATBOT_URL}/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ message: userMessage })
  })

  if (!response.ok) {
    throw new Error(`Flask chatbot error: ${response.status}`)
  }

  const data = await response.json()
  return data.reply
}

/**
 * Generate response using OpenAI API
 */
async function generateAIResponse(userMessage) {
  if (!OPENAI_API_KEY) {
    throw new Error('OpenAI API key not configured')
  }

  const messages = [
    { role: 'system', content: CAMPUS_CONTEXT },
    ...conversationHistory.slice(-MAX_HISTORY),
    { role: 'user', content: userMessage }
  ]

  const response = await fetch(OPENAI_API_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${OPENAI_API_KEY}`
    },
    body: JSON.stringify({
      model: 'gpt-3.5-turbo',
      messages,
      max_tokens: 250,
      temperature: 0.7
    })
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.error?.message || 'AI service unavailable')
  }

  const data = await response.json()
  return data.choices[0].message.content.trim()
}

/**
 * Rule-based fallback for offline mode or AI failures
 */
async function generateRuleBasedResponse(userMessage) {
  const msg = userMessage.toLowerCase()
  
  // Try to match FAQ first
  try {
    const faqData = await getFAQEntries()
    for (const faq of faqData.data || []) {
      if (faq.question && msg.includes(faq.question.toLowerCase().substring(0, 10))) {
        return faq.answer
      }
      // Check keywords
      if (faq.keywords) {
        const keywords = faq.keywords.split(',').map(k => k.trim().toLowerCase())
        if (keywords.some(k => msg.includes(k))) {
          return faq.answer
        }
      }
    }
  } catch {
    // Continue to keyword matching
  }

  // Keyword-based responses
  if (msg.includes('mst')) {
    return 'The MST Building is our main 4-floor academic building at the center of campus. It houses classrooms, computer labs (CL1-CL10 on 3F), and offices. Use the Map tab to see the floor plan!'
  }
  
  if (msg.includes('jst')) {
    return 'JST Building has 4 floors at the back of campus with lecture rooms, laboratories, and seminar areas. Check the Map tab for details.'
  }
  
  if (msg.includes('rst')) {
    return 'RST Building is our 3-floor administrative building. 1F: Registrar/Accounting, 2F: Guidance/Safety/Student Affairs, 3F: IT offices. Located left-bottom from the main gate.'
  }
  
  if (msg.includes('library')) {
    return 'The Library is on the ground floor left wing. Open Mon-Fri 8AM-6PM, Sat 8AM-12PM. It has 2 floors with study areas and digital resources.'
  }
  
  if (msg.includes('registrar')) {
    return 'Registrar Office is on the 1st floor of RST Building with 7 service windows. Hours: Mon-Fri 8AM-5PM.'
  }
  
  if (msg.includes('cl') || msg.includes('computer lab')) {
    return 'Computer Labs CL1-CL10 are on the 3rd floor of MST Building. Use the Navigate tab to get directions from your current location!'
  }
  
  if (msg.includes('canteen') || msg.includes('cafeteria')) {
    return 'The Cafeteria is between the MST Building and Gymnasium, open 7AM-6PM daily serving meals and snacks.'
  }
  
  if (msg.includes('comfort room') || msg.includes('restroom') || msg.includes('cr')) {
    return 'Comfort rooms are on every floor of all buildings (MST, JST, RST), typically near stairwells for easy access.'
  }
  
  if (msg.includes('navigate') || msg.includes('direction') || msg.includes('where is')) {
    return 'Use the Navigate tab for turn-by-turn directions! Enter your starting point and destination to see the shortest route across campus.'
  }
  
  if (msg.includes('qr') || msg.includes('scan')) {
    return 'Use the QR Scanner to scan codes at buildings and rooms for quick info. The app also works offline after your first visit!'
  }
  
  if (msg.includes('offline')) {
    return 'TechnoPath works offline! Once you\'ve loaded the app while online, you can use the map, navigation, and room info without internet. Your feedback will sync when you reconnect.'
  }

  // Default response
  return "I'm here to help with SEAIT campus info! Ask about:\n• Buildings (MST, JST, RST)\n• Computer Labs (CL1-CL10)\n• Offices (Registrar, CICT, Guidance)\n• Facilities (Library, Cafeteria, Gym)\nOr use the Navigate tab for directions!"
}

/**
 * Main chat function - tries Flask first, then OpenAI, then falls back to rules
 */
export async function sendMessage(userMessage) {
  if (!userMessage?.trim()) {
    throw new Error('Message is required')
  }

  // Add to history
  conversationHistory.push({ role: 'user', content: userMessage })
  await saveToHistory('user', userMessage)

  let response
  let source = 'flask'

  if (isOnline()) {
    // Try Flask chatbot first
    try {
      response = await generateFlaskResponse(userMessage)
    } catch (flaskErr) {
      console.log('[AI Chatbot] Flask failed, trying OpenAI:', flaskErr.message)
      
      // Try OpenAI as secondary
      if (OPENAI_API_KEY) {
        try {
          response = await generateAIResponse(userMessage)
          source = 'ai'
        } catch (aiErr) {
          console.log('[AI Chatbot] OpenAI failed, using fallback:', aiErr.message)
          response = await generateRuleBasedResponse(userMessage)
          source = 'fallback'
        }
      } else {
        response = await generateRuleBasedResponse(userMessage)
        source = 'fallback'
      }
    }
  } else {
    // Offline mode - use rule-based
    response = await generateRuleBasedResponse(userMessage)
    source = 'offline'
  }

  // Add response to history
  conversationHistory.push({ role: 'assistant', content: response })
  await saveToHistory('assistant', response)

  // Trim history if too long
  if (conversationHistory.length > MAX_HISTORY * 2) {
    conversationHistory.splice(0, conversationHistory.length - MAX_HISTORY * 2)
  }

  return {
    reply: response,
    source,
    isOffline: !isOnline()
  }
}

/**
 * Clear conversation history
 */
export function clearHistory() {
  conversationHistory.length = 0
}

/**
 * Get chatbot status
 */
export function getStatus() {
  return {
    isOnline: isOnline(),
    hasFlaskUrl: !!FLASK_CHATBOT_URL,
    hasAIKey: !!OPENAI_API_KEY,
    historyLength: conversationHistory.length,
    isAIEnabled: isOnline() && (!!FLASK_CHATBOT_URL || !!OPENAI_API_KEY)
  }
}

export default {
  sendMessage,
  clearHistory,
  getStatus,
  initChatHistory
}
