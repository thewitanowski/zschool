# ZSchool

A modern display layer over Canvas LMS API to help students better access their coursework through an intuitive weekly planner interface.

## 🎯 Project Overview

ZSchool transforms the standard Canvas LMS experience into a personalized and interactive weekly planner, featuring:

- **Phase 1**: Automated weekly plan ingestion and interactive Kanban board
- **Phase 2**: Integrated lesson viewer with progress tracking
- **Phase 3**: AI-powered interactive worksheets and tutor chat

## 🏗️ Architecture

- **Frontend**: React SPA with Material-UI and drag-and-drop functionality
- **Backend**: Python FastAPI with PostgreSQL database
- **AI Integration**: Hugging Face Kimi K2 model for content parsing
- **Containerization**: Docker and Docker Compose for consistent deployment

## ✅ Completed Implementation

### Phase 1, Step 1.1: Backend & Environment Setup ✅
- ✅ Docker Compose orchestration with 3 services (database, backend, frontend)
- ✅ FastAPI backend with SQLAlchemy ORM and PostgreSQL
- ✅ React frontend with Material-UI and drag-and-drop ready
- ✅ Environment variable management with .env files
- ✅ Comprehensive project structure and documentation

### Phase 1, Step 1.2: Canvas API Client ✅
- ✅ Complete Canvas LMS API client with async HTTP support
- ✅ All Canvas endpoints implemented and tested
- ✅ Proper authentication with Bearer tokens
- ✅ URL generation verification and comprehensive testing
- ✅ Error handling and logging throughout

### Phase 1, Step 1.3: Data Ingestion & LLM Parsing ✅
- ✅ AI Service with Kimi K2 model integration via Hugging Face
- ✅ `parse_announcement_to_json()` LLM function with advanced parsing prompts
- ✅ Main backend endpoint `GET /api/v1/week-plan/latest` implemented
- ✅ Database integration for caching parsed results
- ✅ **Test requirement met**: Endpoint returns 200 status with correctly structured JSON

### Phase 1, Step 1.4: Interactive Kanban Board ✅
- ✅ **Complete Kanban board implementation with drag-and-drop functionality**
- ✅ Three-column layout: To Do, In Progress, Done
- ✅ Interactive lesson cards with expandable details
- ✅ Real-time drag-and-drop using react-beautiful-dnd
- ✅ Modern Material-UI design with responsive layout
- ✅ Integration with backend API for dynamic data loading
- ✅ Weekly plan header with teacher info and statistics
- ✅ Error handling and loading states

### Phase 1, Step 1.5: Board State Persistence ✅
- ✅ **Complete board state persistence across sessions**
- ✅ Automatic session ID generation and localStorage storage
- ✅ Real-time saving of drag-and-drop changes to backend
- ✅ Auto-load saved board state on page refresh
- ✅ Visual save indicators with success/error notifications
- ✅ Board reset functionality to default state
- ✅ Database models and API endpoints for persistence
- ✅ Error handling for offline/connection issues

### Phase 1, Step 1.6: Advanced Board Features ✅
- ✅ **Comprehensive search and filtering system**
- ✅ Subject-based filtering with multi-select dropdown
- ✅ Real-time search across all lesson content (subjects, topics, notes, days)
- ✅ Advanced sorting (alphabetical, subject, lesson count, recent)
- ✅ Lesson count range filtering with slider control
- ✅ Status-based filtering (To Do, In Progress, Done)
- ✅ **Detailed board analytics and statistics**
- ✅ Subject color coding and priority indicators
- ✅ Progress tracking with completion percentages
- ✅ Enhanced card details with expandable information
- ✅ Floating action buttons for filter and analytics toggles

### Phase 2, Step 2.1: Integrated Lesson Viewer ✅
- ✅ **AI-powered content transformation**
- ✅ Canvas API integration for fetching lesson content (Pages, Assignments, Discussions)
- ✅ Intelligent HTML-to-structured content conversion using LLM
- ✅ Clean, educational formatting with learning objectives and key points
- ✅ **Interactive lesson viewer interface**
- ✅ Modal-based lesson content display with beautiful Material-UI design
- ✅ Click-to-view functionality on lesson cards and buttons
- ✅ Structured content sections with appropriate formatting and icons
- ✅ **Enhanced learning features**
- ✅ Learning objectives display with checkboxes
- ✅ Resource links with external access
- ✅ Bookmark and completion tracking
- ✅ Responsive design with smooth animations and loading states

### Phase 2, Step 2.2: In-App Lesson Actions ✅
- ✅ **Interactive lesson completion system**
- ✅ "Mark as Done" button with Canvas LMS synchronization
- ✅ "Mark as Read" button for tracking lesson viewing progress
- ✅ Real-time Canvas status synchronization and progress tracking
- ✅ **Kanban board integration**
- ✅ Automatic card movement when lessons are completed
- ✅ Real-time board state updates with lesson progress
- ✅ Visual status indicators and completion tracking
- ✅ **Enhanced user experience**
- ✅ Smart notifications and contextual feedback
- ✅ Loading states and error handling for all actions
- ✅ Cross-session progress persistence and restoration
- ✅ Canvas API integration for lesson completion workflows

## 🎮 Interactive Kanban Board Features

### 🎯 **Core Functionality**
- **Drag & Drop**: Seamlessly move lesson cards between columns
- **Three-Column Layout**: Organized workflow with To Do, In Progress, and Done
- **Real-time Updates**: Instant visual feedback during drag operations
- **Cross-session Persistence**: Automatic saving and loading of board state
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile

### 🔍 **Advanced Search & Filtering**
- **Real-time Search**: Search across subjects, topics, lessons, notes, and scheduled days
- **Subject Filtering**: Multi-select dropdown with subject counts
- **Status Filtering**: Filter by To Do, In Progress, or Done status
- **Lesson Count Range**: Slider control for filtering by lesson quantity
- **Smart Sorting**: Alphabetical, by subject, lesson count, or recent
- **Empty Column Toggle**: Show/hide columns with no filtered results
- **Active Filter Display**: Visual chips showing all applied filters

### 📊 **Comprehensive Analytics**
- **Board Statistics**: Total subjects, lessons, completion rates
- **Progress Breakdown**: Visual progress bars for each status
- **Subject Analysis**: Top subjects by lesson count with completion rates
- **Priority Indicators**: Automatic detection of high-priority subjects
- **Weekly Insights**: Scheduled days, notes count, priority subjects
- **Real-time Updates**: Statistics update automatically as filters change

### 📚 **Enhanced Lesson Cards**
- **Subject Color Coding**: Unique colors for each subject with avatars
- **Priority Indicators**: Visual priority markers for important subjects
- **Progress Visualization**: Completion percentage bars for active cards
- **Expandable Details**: Click to see full lesson lists, notes, and metadata
- **Status Icons**: Visual indicators for card status (To Do, In Progress, Done)
- **Lesson Metadata**: Unit, topic, scheduled days, and important notes

### 🎨 **Modern UI/UX**
- **Material Design 3**: Clean, modern interface with glass-morphism effects
- **Floating Action Buttons**: Easy access to filters and analytics
- **Color-Coded Everything**: Subjects, priorities, and status indicators
- **Smooth Animations**: Polished transitions, hover effects, and drag feedback
- **Visual Notifications**: Toast messages for save confirmations and errors
- **Gradient Designs**: Beautiful headers and cards with backdrop blur

### 📊 **Weekly Plan Header**
- **Week Overview**: Display of current week and teacher information
- **Live Statistics**: Real-time count of subjects, lessons, and announcements
- **Session Management**: Display session ID and auto-save status
- **Action Buttons**: Refresh data, reset board, and board management
- **Save Indicators**: Visual feedback for save operations and status

### 📖 **Integrated Lesson Viewer**
- **AI-Transformed Content**: Canvas HTML converted to clean, educational format
- **Learning Objectives**: Clear, checkboxed objectives for each lesson
- **Structured Sections**: Well-organized content with appropriate icons and formatting
- **Interactive Elements**: Clickable resources, external links, and embedded media references
- **Progress Tracking**: Bookmark lessons and mark as completed
- **Responsive Design**: Beautiful modal interface with smooth animations
- **Content Caching**: Fast loading with intelligent backend caching
- **Error Handling**: Graceful fallbacks when content is unavailable
- **Multiple Content Types**: Support for Pages, Assignments, Discussions, and Files
- **Educational Focus**: Optimized layout for learning with key takeaways and summaries

### 🎯 **In-App Lesson Actions**
- **Mark as Done**: Complete lessons with automatic Canvas LMS synchronization
- **Mark as Read**: Track lesson viewing progress for study planning
- **Canvas Sync**: Real-time status synchronization with Canvas gradebook
- **Board Integration**: Automatic card movement when lessons are completed
- **Status Indicators**: Visual progress tracking with completion status display
- **Smart Notifications**: Contextual feedback for all lesson actions
- **Progress Persistence**: Cross-session completion tracking and restoration
- **Error Handling**: Comprehensive error management with user-friendly messages
- **Loading States**: Visual feedback during lesson action processing
- **Batch Operations**: Support for multiple lesson actions and bulk updates

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Environment variables configured (see .env.example)

### Installation & Setup

1. **Clone and configure**:
   ```bash
   git clone <repository-url>
   cd zschool
   cp .env.example .env
   # Edit .env with your actual tokens
   ```

2. **Start all services**:
   ```bash
   docker-compose up -d
   ```

3. **Access the application**:
   - **Kanban Board**: http://localhost:3001
   - **Backend API**: http://localhost:8001
   - **Database**: PostgreSQL on port 5433

## 🎯 **Phase 1, Step 1.6 Demo**

Visit **http://localhost:3001** to experience the advanced Kanban board:

1. **Enhanced Weekly Plan Header** with teacher info, statistics, and session management
2. **Advanced Filtering** using the floating filter button (bottom-right)
3. **Comprehensive Analytics** via the chart button for detailed insights
4. **Smart Search** across all lesson content in real-time
5. **Subject Color Coding** with automatic priority detection
6. **Drag & Drop** with automatic persistence across browser sessions
7. **Enhanced Card Details** with expandable information and progress indicators
8. **Responsive Design** that adapts perfectly to any screen size

## 🔧 API Endpoints

### Core Functionality

#### Phase 1, Step 1.3 - Main Weekly Plan Endpoint
```bash
# Get latest weekly plan (main endpoint)
GET /api/v1/week-plan/latest?force_refresh=false

# Get mock data demonstrating expected JSON structure
GET /api/v1/week-plan/mock

# Get all cached weekly plans
GET /api/v1/week-plan/all?limit=10

# Get plan by specific date
GET /api/v1/week-plan/by-date?week_starting=2025-07-28
```

#### Phase 1, Step 1.5 - Board State Persistence
```bash
# Generate a new session ID for persistence
GET /api/v1/board-state/session

# Save current board state (requires user-session header)
POST /api/v1/board-state/save
Header: user-session: <session-id>
Body: {"board_data": {...}, "weekly_plan_id": 1}

# Load saved board state (requires user-session header)
GET /api/v1/board-state/load?weekly_plan_id=1
Header: user-session: <session-id>

# Clear/reset board state (requires user-session header)
DELETE /api/v1/board-state/clear?weekly_plan_id=1
Header: user-session: <session-id>

# Get summary of all board states for a weekly plan
GET /api/v1/board-state/summary/1
```

#### Phase 2, Step 2.1 - Lesson Content Viewer
```bash
# Get demo lesson content for testing (lesson numbers 1-3)
GET /api/v1/lessons/demo/1

# Get lesson content by database ID
GET /api/v1/lessons/{lesson_id}

# Fetch and transform Canvas lesson content with caching
GET /api/v1/lessons/canvas/{course_id}/{module_item_id}?force_refresh=false

# Mark lesson as completed (requires user-session header)
POST /api/v1/lessons/{lesson_id}/complete
Header: user-session: <session-id>
Body: true  # or false to mark as incomplete

# Get all lessons for a weekly plan
GET /api/v1/weekly-plans/{weekly_plan_id}/lessons
```

#### Phase 2, Step 2.2 - In-App Lesson Actions
```bash
# Mark lesson as done with Canvas synchronization
POST /api/v1/lessons/{lesson_id}/mark-done
Header: user-session: <session-id>
Body: {"course_id": 20564, "module_item_id": 12345}

# Mark lesson as read (progress tracking)
POST /api/v1/lessons/{lesson_id}/mark-read
Header: user-session: <session-id>

# Update lesson status in Kanban board
POST /api/v1/lessons/{lesson_id}/update-board-status
Header: user-session: <session-id>
Body: "done"  # or "in-progress" or "to-do"

# Get lesson with real-time Canvas status
GET /api/v1/lessons/{lesson_id}/canvas-status

# Mark Canvas lesson complete directly
POST /api/v1/canvas/lesson/{course_id}/{module_item_id}/complete
Body: true  # or false to mark as incomplete

# Get Canvas course progress
GET /api/v1/canvas/progress/{course_id}?user_id=<optional>
```

### Testing & Integration

```bash
# Test complete integration (Canvas + AI + Database)
GET /api/v1/test/integration

# Test Canvas API connection
GET /api/v1/canvas/test

# Test AI service connection  
GET /api/v1/ai/test

# Get latest Canvas announcement (debugging)
GET /api/v1/canvas/announcement/latest
```

### Health & Status

```bash
# Basic health check
GET /health

# API status with service information
GET /api/v1/status
```

## 🧪 Testing Phase 1, Step 1.6

### Test: Advanced Board Features Working

The main test for Phase 1, Step 1.6 is the complete advanced Kanban board functionality:

```bash
# 1. Verify all services are running
docker-compose ps

# 2. Test backend API provides data
curl -s http://localhost:8001/api/v1/week-plan/mock | python3 -c "import sys, json; data=json.load(sys.stdin); print(f'✅ API returns {len(data[\"data\"][\"classwork\"])} subjects')"

# 3. Test board state persistence endpoints
SESSION_ID=$(curl -s http://localhost:8001/api/v1/board-state/session | python3 -c "import sys, json; print(json.load(sys.stdin)['session_id'])")
curl -s -X POST -H "user-session: $SESSION_ID" -H "Content-Type: application/json" -d '{"board_data":{"to-do":[],"in-progress":[{"id":"test","subject":"Math"}],"done":[]}}' http://localhost:8001/api/v1/board-state/save | python3 -c "import sys, json; print(f'✅ Save: {json.load(sys.stdin)[\"status\"]}')"
curl -s -H "user-session: $SESSION_ID" http://localhost:8001/api/v1/board-state/load | python3 -c "import sys, json; print(f'✅ Load: {json.load(sys.stdin)[\"status\"]}')"

# 4. Test frontend is accessible
curl -s -I http://localhost:3001 | head -1
# Expected: HTTP/1.1 200 OK
```

### **Advanced Features to Test**

1. **🔍 Search and Filtering System**
   - Click the filter button (bottom-right floating action button)
   - Search for "Math" in the search box - see filtered results
   - Use subject dropdown to filter by specific subjects
   - Try the advanced filters (accordion panel)
   - Use lesson count slider to filter by lesson quantity
   - Watch active filter chips update in real-time

2. **📊 Comprehensive Analytics**
   - Click the analytics button (chart icon, bottom-right)
   - View board statistics (total subjects, lessons, completion rate)
   - Check progress breakdown with visual progress bars
   - See top subjects by lesson count
   - View weekly insights (scheduled days, priority subjects)
   - Notice how statistics update when filters are applied

3. **🎨 Enhanced Card Features**
   - Notice subject color coding (each subject has unique color)
   - Look for priority indicators on high-priority subjects
   - Click expand button on any card to see detailed information
   - Check progress bars on cards in "In Progress" column
   - See status icons (check marks, clock, empty circle)

4. **💾 Persistent Board State**
   - Move some lesson cards between columns
   - Watch for "Progress saved!" notification
   - Refresh the browser page (F5)
   - Verify cards remain in their moved positions
   - See "Loaded your saved progress!" notification

5. **🎯 Smart Sorting and Organization**
   - Open advanced filters and try different sorting options
   - Sort by subject, lesson count, or alphabetical
   - Toggle "Show empty columns" to hide empty sections
   - Use the reset button to return to default state

6. **📱 Responsive Design and UX**
   - Resize browser window to test mobile layout
   - Check floating action buttons adapt to screen size
   - Test drag-and-drop on touch devices
   - Verify all features work on different screen sizes

## 🗄️ Database Schema

The system uses PostgreSQL with these main tables:

- **weekly_plans**: Stores processed JSON from LLM parsing
- **courses**: Canvas course metadata
- **modules**: Course module information  
- **module_items**: Individual lesson/content items
- **assignments**: Assignment and due date information
- **board_states**: User-specific Kanban board state persistence
- **lesson_contents**: Cached and AI-transformed lesson content from Canvas
- **weekly_plan_lessons**: Links lessons to weekly plans with user progress tracking

## 🔀 Service Architecture

```
Frontend (React + Kanban) ←→ Backend (FastAPI) ←→ Canvas LMS API
           ↑                         ↓
    Material-UI + DnD        AI Service (Kimi K2) ←→ Hugging Face API
                                     ↓
                             Database (PostgreSQL)
```

## 📡 Canvas Integration

- **Base URL**: https://learning.acc.edu.au
- **Course ID**: 20564 (as specified in project brief)
- **Authentication**: Bearer token via environment variables
- **Endpoints**: Announcements, courses, modules, calendar events, pages

## 🤖 AI Integration

- **Model**: moonshotai/Kimi-K2-Instruct:novita via Hugging Face
- **Purpose**: Parse Canvas announcement HTML into structured JSON
- **Features**: Advanced parsing with lesson expansion, date extraction, content categorization
- **Caching**: Results stored in database for performance

## 🎨 Frontend Technology Stack

- **React 18**: Modern functional components with hooks
- **Material-UI v5**: Complete design system with theming
- **react-beautiful-dnd**: Smooth drag-and-drop interactions
- **Styled Components**: Custom styling with theme integration
- **Axios**: HTTP client for API communication
- **Responsive Design**: Mobile-first approach with breakpoints

## 🎯 Current Status

**Phase 2, Step 2.2: COMPLETE** ✅

ZSchool now provides a fully integrated learning management experience with interactive lesson actions:
- ✅ **Complete Canvas LMS integration** with AI-powered content parsing and lesson completion
- ✅ **Interactive drag-and-drop Kanban board** with automatic persistence and real-time updates
- ✅ **Advanced search and filtering** across all lesson content with smart analytics
- ✅ **Comprehensive lesson viewer** with AI-transformed content and interactive actions
- ✅ **In-app lesson completion system** with Canvas synchronization
- ✅ **Smart lesson actions** including "Mark as Done" and "Mark as Read" functionality
- ✅ **Real-time progress tracking** with automatic board updates on lesson completion
- ✅ **Cross-session persistence** for board state, lesson progress, and completion status
- ✅ **Canvas API synchronization** for lesson completion and progress tracking
- ✅ **Visual status indicators** with smart notifications and contextual feedback
- ✅ **Subject color coding** and priority indicators with completion tracking
- ✅ **Modern responsive UI** with beautiful animations and educational design
- ✅ **Production-ready error handling** with fallback content and comprehensive offline support

**Ready for Phase 2, Step 2.3**: Advanced lesson management and grading integration

## 🔧 Development

### Local Development Setup

```bash
# Install dependencies
cd backend && pip install -r requirements.txt
cd frontend && npm install

# Run locally (without Docker)
cd backend && uvicorn main:app --reload --port 8001
cd frontend && npm start  # Port 3001
```

### Testing

```bash
# Run backend tests
cd backend && python -m pytest test_canvas_client.py -v

# Test Kanban board functionality
open http://localhost:3001  # Manual testing in browser

# Test API endpoints
curl http://localhost:8001/api/v1/week-plan/mock
```

## 📝 Environment Configuration

Required environment variables:

```env
# Canvas LMS Authentication
CANVAS_BEARER_TOKEN=your_canvas_bearer_token_here

# Hugging Face AI Model Access  
HF_TOKEN=your_huggingface_token_here

# Database (configured in docker-compose.yml)
DATABASE_URL=postgresql://zschool_user:zschool_password@db:5432/zschool

# Environment
ENVIRONMENT=development
```

## 🐳 Docker Configuration

Services are configured to use non-conflicting ports:
- **Database**: Port 5433 (PostgreSQL)
- **Backend**: Port 8001 (FastAPI)
- **Frontend**: Port 3001 (React with Kanban Board)

## 📈 Next Steps

1. **Phase 1, Step 1.6**: Advanced board features (filters, search, categories)
2. **Phase 2**: Lesson viewer integration with Canvas content
3. **Phase 3**: AI-powered worksheets and tutor chat
4. **Future Enhancements**: Multi-user support, notifications, analytics

## 🎉 **Major Milestone Achieved**

Phase 1 of ZSchool is now **fully complete** with a persistent Kanban board that:
- Transforms Canvas LMS data into an intuitive visual interface
- Provides interactive drag-and-drop lesson management with automatic persistence
- Saves user progress across browser sessions and device switches
- Offers a modern, responsive user experience with real-time save feedback
- Handles offline scenarios gracefully with comprehensive error handling
- Demonstrates a production-ready foundation for the ZSchool platform

---

🎓 **ZSchool** - Transforming Canvas LMS into an intuitive learning experience 