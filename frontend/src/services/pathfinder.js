// Dijkstra's algorithm — ported from pathfinder.dart
// Works fully offline using navigation_nodes and navigation_edges from IndexedDB

import { getNavigationData } from './offlineData.js'

export function dijkstra(nodes, edges, startId, endId) {
  const distances = {}
  const previous = {}
  const visited = new Set()
  const queue = []

  nodes.forEach(n => {
    distances[n.id] = Infinity
    previous[n.id] = null
  })
  distances[startId] = 0
  queue.push({ id: startId, dist: 0 })

  while (queue.length > 0) {
    queue.sort((a, b) => a.dist - b.dist)
    const { id: currentId } = queue.shift()

    if (visited.has(currentId)) continue
    visited.add(currentId)

    if (currentId === endId) break

    const neighbors = edges.filter(
      e => (!e.is_deleted) && (
        e.from_node_id === currentId ||
        (e.is_bidirectional && e.to_node_id === currentId)
      )
    )

    for (const edge of neighbors) {
      const neighborId = edge.from_node_id === currentId ? edge.to_node_id : edge.from_node_id
      if (visited.has(neighborId)) continue
      const newDist = distances[currentId] + edge.distance
      if (newDist < distances[neighborId]) {
        distances[neighborId] = newDist
        previous[neighborId] = currentId
        queue.push({ id: neighborId, dist: newDist })
      }
    }
  }

  // Reconstruct path
  const path = []
  let current = endId
  while (current !== null) {
    path.unshift(current)
    current = previous[current]
  }

  if (path[0] !== startId) return null // No path found
  return { path, distance: distances[endId] }
}

/**
 * Find path between two locations using backend navigation graph
 * @param {string} startName - Starting location name
 * @param {string} endName - Destination location name
 * @returns {Promise<{path: Array, totalDistance: number, totalTime: number, steps: Array}>}
 */
export async function findPath(startName, endName) {
  try {
    // Get navigation data from backend/IndexedDB
    const navData = await getNavigationData()
    const nodes = navData.nodes
    const edges = navData.edges

    if (!nodes || nodes.length === 0) {
      throw new Error('No navigation data available')
    }

    // Find nodes by name (or map_svg_id)
    const startNode = nodes.find(n => 
      n.name?.toLowerCase() === startName.toLowerCase() || 
      n.map_svg_id?.toLowerCase() === startName.toLowerCase()
    )
    const endNode = nodes.find(n => 
      n.name?.toLowerCase() === endName.toLowerCase() || 
      n.map_svg_id?.toLowerCase() === endName.toLowerCase()
    )

    if (!startNode) {
      throw new Error(`Start location "${startName}" not found`)
    }
    if (!endNode) {
      throw new Error(`Destination "${endName}" not found`)
    }

    // Run Dijkstra
    const result = dijkstra(nodes, edges, startNode.id, endNode.id)
    
    if (!result) {
      throw new Error('No path found between locations')
    }

    // Build path with node details
    const pathNodes = result.path.map(nodeId => {
      const node = nodes.find(n => n.id === nodeId)
      return {
        id: node.id,
        name: node.name,
        x: node.x_position || 0.5,
        y: node.y_position || 0.5,
        floor: node.floor || 1
      }
    })

    // Generate turn-by-turn steps
    const steps = generateSteps(pathNodes, result.distance)

    // Estimate time (assume 1.4 m/s walking speed + 30s per turn)
    const walkingTime = result.distance / 1.4 / 60 // minutes
    const turnTime = (pathNodes.length - 1) * 0.5 // 30s per transition
    const totalTime = Math.max(1, Math.round(walkingTime + turnTime))

    return {
      path: pathNodes,
      totalDistance: Math.round(result.distance),
      totalTime: totalTime,
      steps: steps
    }
  } catch (err) {
    console.error('[Pathfinder] Error finding path:', err)
    throw err
  }
}

/**
 * Generate turn-by-turn directions from path nodes
 */
function generateSteps(pathNodes, totalDistance) {
  if (pathNodes.length === 0) return []
  
  const steps = []
  
  // Start step
  steps.push({
    instruction: `Start at ${pathNodes[0].name}`,
    distance: ''
  })

  // Intermediate steps
  for (let i = 1; i < pathNodes.length - 1; i++) {
    const prev = pathNodes[i - 1]
    const curr = pathNodes[i]
    const next = pathNodes[i + 1]
    
    // Calculate segment distance
    const dx = (curr.x - prev.x) * 200 // scale factor
    const dy = (curr.y - prev.y) * 200
    const segmentDist = Math.round(Math.sqrt(dx * dx + dy * dy))
    
    // Determine turn direction
    let turn = 'Continue'
    if (next) {
      const angle = calculateAngle(prev, curr, next)
      if (angle > 30) turn = 'Turn right'
      else if (angle < -30) turn = 'Turn left'
      else if (Math.abs(angle) > 150) turn = 'Make a U-turn'
    }
    
    steps.push({
      instruction: `${turn} toward ${curr.name}`,
      distance: `~${segmentDist}m`
    })
  }

  // End step
  if (pathNodes.length > 1) {
    steps.push({
      instruction: `Arrive at ${pathNodes[pathNodes.length - 1].name}`,
      distance: ''
    })
  }

  return steps
}

/**
 * Calculate turn angle between three points
 */
function calculateAngle(p1, p2, p3) {
  const dx1 = p2.x - p1.x
  const dy1 = p2.y - p1.y
  const dx2 = p3.x - p2.x
  const dy2 = p3.y - p2.y
  
  const angle1 = Math.atan2(dy1, dx1)
  const angle2 = Math.atan2(dy2, dx2)
  
  let angle = (angle2 - angle1) * 180 / Math.PI
  if (angle > 180) angle -= 360
  if (angle < -180) angle += 360
  
  return angle
}
