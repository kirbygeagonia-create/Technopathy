# CHAPTER 1 - CORRECTED VERSION
## THE PROBLEM AND ITS BACKGROUND

---

### Introduction

The TechnoPath: SEAIT Guide Map and Navigation System is a Progressive Web Application (PWA) designed to display the complete layout of the South East Asian Institute of Technology, Inc. (SEAIT) campus, located at Barangay Crossing Rubber, National Highway, Tupi, South Cotabato, 9505, Philippines. The study provides interactive two-dimensional (2D) map of the campus buildings, including the RST, MST, and JST buildings, the Basic Education building, the gymnasium, canteens, playground, and other campus facilities, with each map containing clearly labeled rooms, offices, and key institutional areas organized by floor level. The study further incorporates a QR code access point posted at the main gate of the SEAIT campus, enabling students, faculty, and visitors to immediately load the campus guide map upon arrival by scanning the code with a mobile device, without requiring prior application installation or knowledge of the application URL.

The study operates under a structured **role-based administrative backend** with a four-tier hierarchy:

1. **Super Admin (Safety and Security Office)** - Full system access including structural building information management
2. **Dean (College Dean)** - Department-level management and oversight authority with direct publication rights for department-scoped announcements
3. **Program Head/Basic Ed Head** - Department-specific data management (classroom assignments, departmental announcements) with approval workflow for campus-wide announcements
4. **Guest Users (Students, Visitors, Faculty)** - Read-only access to navigation features

An **AI Virtual Guide** feature is integrated into the study to deliver conversational navigation assistance, allowing users to describe their intended destination in natural language and receive directional guidance based on stored campus navigation data. The system operates in both **online mode** (using external AI API) and **offline mode** (using local FAQ database with keyword matching), thereby supporting independent wayfinding across the entire SEAIT campus grounds and buildings regardless of internet connectivity.

---

### CORRECTED Technology Stack

**Frontend Technology:**
- **Vue.js 3** - Progressive JavaScript framework for building user interfaces
- **Vue Router** - Official router for Vue.js applications
- **Pinia** - State management library for Vue.js
- **IndexedDB** - Browser-based database for offline data storage
- **Axios** - HTTP client for API communication
- **Leaflet/OpenLayers** - Interactive map library for 2D campus maps

**Backend Technology:**
- **Django 4.2+** - High-level Python web framework
- **Django REST Framework** - Toolkit for building Web APIs
- **Django ORM** - Object-Relational Mapping for database operations
- **PostgreSQL** - Primary production database (SQLite for development)

**Authentication & Security:**
- **Django Authentication System** - PBKDF2 password hashing algorithm
- **JWT (JSON Web Tokens)** - Stateless authentication mechanism
- **django-cors-headers** - Cross-Origin Resource Sharing handling

**AI Chatbot Service:**
- **Python Flask** - Lightweight backend for AI API integration (optional microservice)
- **External AI API** - Online conversational AI service
- **Local FAQ Database** - SQLite-based offline fallback with keyword matching

---

### The Current Problem

The current orientation and navigation process at the SEAIT campus is conducted entirely through manual and informal means, with no structured digital wayfinding system in place to assist individuals entering or moving within the campus premises. However, there are printed tarpaulins specifically in each facility. Hence, no clear guide map, posted signage, or digital reference is available at the campus entrance or within the campus grounds to direct new arrivals toward the buildings, classrooms, offices, or facilities they need to locate.

[Rest of Problem Statement remains the same...]

---

### Objectives of the Study

#### General Objective

The study aims to design and develop the TechnoPath: SEAIT Guide Map and Navigation System for the students, faculty, visitors, and the Safety and Security Office of South East Asian Institute of Technology, Inc. (SEAIT), Barangay Crossing Rubber, National Highway, Tupi, South Cotabato, to provide a centralized, interactive, and digitalized guide map and navigation platform that addresses campus orientation and wayfinding challenges.

#### Special Objectives

1. To be able to display a visual route from the main gate to the different buildings and facilities of SEAIT campus and to show interactive 2D floor maps of the SEAIT buildings with labeled rooms to guide students, faculty, and visitors in locating classrooms, offices, and facilities within the SEAIT campus.

2. To be able to provide a digital platform where SEAIT departmental **Program Head, Basic Ed Head, Dean, and Safety and Security Office** can make announcements and can add, modify, and delete room labels, office designations, and classroom assignments through the administrative backend for accurate and current student, faculty, and visitor reference.

3. To be able to display labeled building maps that highlight the offices, inquiry desks, and key rooms within the SEAIT campus buildings to help students, faculty, and visitors locate them quickly.

4. To be able to provide a scannable QR code posted at the main gate of the SEAIT campus that allows students, faculty, and visitors to immediately access the TechnoPath Guide Map and Navigation System.

5. To be able to provide an AI-powered virtual assistant that answers location-related questions and gives route directions to help students, faculty, and visitors find classrooms, offices, and facilities independently, with **offline fallback capability** using local FAQ database when internet connectivity is unavailable.

---

### CORRECTED Scope of the Study

#### Scope of the Study

The study is developed to address the campus navigation and orientation challenges experienced by students, faculty, visitors, and the Safety and Security Office of South East Asian Institute of Technology, Inc. (SEAIT), Barangay Crossing Rubber, National Highway, Tupi, South Cotabato.

##### 1. Campus Navigation Guide with 2D Building Floor Maps

The study provides an interactive 2D campus ground layout and 2D floor maps of the SEAIT campus buildings using **Vue.js with SVG rendering and Leaflet mapping library**. The feature allows users to view and interact the main gate, campus walkways, and the locations of all buildings, and to navigate individual building floors with labeled rooms, highlighted offices, and key facility markers. The navigation guide also displays visual routes from the main gate to the target buildings to assist users who are visiting the campus for the first time.

##### 2. Building Classroom and Room Updates

The study allows authorized **department Program Head, Basic Ed Head, Dean, and the Safety and Security Office** to add, modify, and delete room labels, office designations, and classroom assignments within the digital building maps through the administrative backend. The feature includes:

- **Role-based access control** with four-tier hierarchy
- **Announcement approval workflow** (campus-wide announcements require Super Admin approval)
- **Soft delete** functionality for data preservation
- **Audit logging** for all administrative actions

The feature ensures that the navigational information displayed to users remains accurate and reflects current institutional arrangements, particularly when room assignments are changed during the academic year.

##### 3. SEAIT Building Room Maps with Highlighted Offices

The study displays labeled maps of the SEAIT campus buildings with highlighted offices, inquiry desks, and key institutional rooms using **interactive map markers and labels** stored in the database. The feature allows users to retrieve the location of specific offices within the building floors, enabling faster and more accurate navigation to administrative and academic service areas without requiring verbal directions from campus personnel.

##### 4. QR Code Access Point (Main Gate)

The study provides a scannable QR code posted at the main gate of the SEAIT campus. The feature allows any user — students, faculty, or visitors — to retrieve and load the campus guide map immediately upon arrival by scanning the code with a mobile device, without requiring a prior application installation or knowledge of the URL. The system uses **deep linking** to direct users to the PWA.

##### 5. AI Chatbot / Virtual Guide

The study provides an AI-powered conversational assistant that responds to location-related queries submitted by users. The feature operates in **dual modes**:

- **Online Mode**: Uses external AI API through Python backend for conversational responses
- **Offline Mode**: Uses local **FAQ database with keyword matching** for navigation assistance when internet connectivity is unavailable

The system automatically detects connectivity status and switches modes seamlessly.

#### CORRECTED Limitations of the Study

The TechnoPath: SEAIT Guide Map and Navigation System is limited to the campus premises of South East Asian Institute of Technology, Inc. (SEAIT) and does not extend to off-campus locations or external facilities. The study operates as a 2D visual map and navigation guide and does not incorporate real-time GPS tracking, augmented reality overlays, or three-dimensional building visualization.

Navigation through the AI Virtual Guide feature is limited to responses based on the stored campus map and location data, and the study is unable to provide answers outside the scope of campus-related queries.

**[CORRECTED]** The system uses **PostgreSQL as the primary production database** with **SQLite for development environments**, not SQLite-only as previously stated.

The building room update module restricts data modification access to authorized administrators only, and the study does not allow public users to add, edit, or delete any campus information. The study does not include real-time event scheduling integration with external institutional management systems.

The accuracy of map information is dependent on the timely updating of room labels and office designations by the authorized administrators, and the study does not automatically reflect physical changes to the campus that are not entered through the administrative backend.

---

### CORRECTED Significance of the Study

The TechnoPath: SEAIT Guide Map and Navigation System holds practical and academic significance for the different groups who are directly and indirectly connected to the South East Asian Institute of Technology, Inc. (SEAIT).

#### Guest Users (Students, Faculty, Visitors)

**[CORRECTED]** The study groups Students, Faculty, and Visitors under a unified **"Guest User"** actor with the following system access:
- Scan QR code at main gate
- View campus ground layout map
- View building floor maps
- Search for rooms and facilities
- Navigate to a destination
- Use AI chatbot for location queries
- Submit anonymous feedback and ratings
- View notifications

The study enables SEAIT students, particularly freshmen and transferees, to locate classrooms, offices, and facilities within the campus through an interactive digital guide. The study reduces confusion and prevents late attendance by providing accurate and updated navigation references before and during class days.

#### Safety and Security Office (Super Admin)

The study serves as a digital management tool that allows the Safety and Security Office to oversee structural building information, including room creation, deletion, and layout configuration. The **Super Admin** role has full system access including:
- Managing all facilities and rooms across departments
- Managing navigation graph (nodes and edges)
- Managing FAQ/Chatbot knowledge base
- Managing QR code access points
- Approving campus-wide announcements
- Sending system notifications
- Managing admin accounts
- Viewing all feedback and audit logs

#### Program Head and Basic Ed Head

**[CORRECTED]** The study provides the **Program Head (College Program Head)** and **Basic Ed Head (Basic Education Head)** with department-level administrative access:
- Managing own department's classroom assignments
- Posting department-scoped announcements (direct publication)
- Posting campus-wide announcements (requires Super Admin approval)
- Viewing department-level reports and feedback

#### Dean (College Dean)

**[CORRECTED]** The **Dean** serves as an oversight authority with the following capabilities:
- Managing own department's rooms and facilities
- Posting department-scoped announcements (direct publication)
- Posting campus-wide announcements (requires Super Admin approval)
- Viewing all departmental reports and feedback
- Viewing audit logs (department-level)
- Monitoring data integrity across departments

#### Researchers and Future Researchers

[Remain the same...]

---

### CORRECTED Definition of Terms

**SEAIT** — South East Asian Institute of Technology, Inc., the educational institution located at Barangay Crossing Rubber, National Highway, Tupi, South Cotabato, 9505, Philippines, where the TechnoPath Guide Map and Navigation System is developed and implemented.

**Vue.js** — A progressive JavaScript framework used as the frontend technology of TechnoPath to build the user interface components, handle routing, and manage application state through the Pinia store.

**Django** — A high-level Python web framework used as the primary backend technology of TechnoPath, providing the ORM, authentication system, and REST API endpoints.

**Django REST Framework** — A powerful and flexible toolkit for building Web APIs, used in TechnoPath to expose database resources as RESTful endpoints for the Vue.js frontend.

**PostgreSQL** — An advanced open-source relational database used as the **primary production database** for TechnoPath, providing robust data storage, complex queries, and transaction support.

**SQLite** — A lightweight, serverless database used as the **development database** and for **local FAQ storage** in offline mode.

**Progressive Web Application (PWA)** — A type of application software delivered through the web, built using common web technologies including HTML, CSS, and JavaScript, intended to work on any platform that uses a standards-compliant browser.

**IndexedDB** — A low-level API for client-side storage of significant amounts of structured data, used in TechnoPath for offline data persistence in the browser.

**Super Admin** — The highest administrative role in TechnoPath, assigned to the Safety and Security Office, with full system access including managing all departments, approving campus-wide announcements, and viewing all audit logs.

**Dean** — An administrative role in TechnoPath assigned to College Deans, with department-level management authority and oversight capabilities, including the ability to post department-scoped announcements directly while requiring approval for campus-wide announcements.

**Program Head** — An administrative role in TechnoPath assigned to College Program Heads, with authority to manage department-specific rooms and announcements, requiring approval for campus-wide announcements.

**Basic Ed Head** — An administrative role in TechnoPath assigned to the Basic Education Department Head, with the same permissions as Program Head for managing Basic Education department data.

**Guest User** — A consolidated user category in TechnoPath encompassing Students, Faculty, and Visitors, with read-only access to navigation features, maps, and AI chatbot.

**Role-Based Access Control (RBAC)** — A security approach used in TechnoPath that assigns specific data management permissions to different user roles (Super Admin, Dean, Program Head, Basic Ed Head), ensuring appropriate access levels based on institutional responsibilities.

**Announcement Approval Workflow** — A process in TechnoPath where campus-wide announcements created by Dean, Program Head, or Basic Ed Head require approval from the Super Admin before publication, while department-scoped announcements can be published directly by the respective department heads.

**Dijkstra's Algorithm** — A shortest-path computation algorithm implemented in the TechnoPath navigation system to calculate the most efficient route between two locations on the campus map.

**Offline-First Architecture** — A system design approach wherein TechnoPath stores all essential data locally (IndexedDB/SQLite) to function fully without an active internet connection, with automatic synchronization when connectivity is restored.

**FAQ (Frequently Asked Questions) Database** — A local database stored on the client device containing pre-written question-and-answer pairs covering common campus navigation queries, serving as the fallback knowledge source for the AI chatbot when offline.

**Keyword Matching** — A text-processing technique used in the offline mode of TechnoPath wherein the user's submitted query is compared against pre-defined keywords associated with FAQ entries in the local database.

**Soft Delete** — A data management technique used in TechnoPath wherein a deleted record is marked as inactive using a boolean flag (is_deleted) rather than being permanently removed, preserving data integrity and allowing restoration.

**Audit Log** — A comprehensive record of all administrative actions performed in the TechnoPath system, tracking who made changes, what was changed, and when, for accountability and data integrity purposes.

[Remaining definitions stay the same...]

---

*CHAPTER 1 - CORRECTED VERSION*
*Match actual TechnoPath V4 System Implementation*
