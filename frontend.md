# Frontend Documentation - ZSchool Kanban Board

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Component Structure](#component-structure)
3. [State Management](#state-management)
4. [API Integration](#api-integration)
5. [Drag & Drop Implementation](#drag--drop-implementation)
6. [Styling & Theme](#styling--theme)
7. [Data Flow](#data-flow)
8. [Key Features](#key-features)
9. [Component API Reference](#component-api-reference)
10. [Customization Guide](#customization-guide)

## Architecture Overview

The frontend is a React 18 application built with Material-UI (MUI) components and `react-beautiful-dnd` for drag-and-drop functionality. It follows a component-based architecture with centralized state management.

### Tech Stack
- **React**: 18.2.0 (Hooks-based functional components)
- **Material-UI**: 5.14.18 (Design system and components)
- **react-beautiful-dnd**: 13.1.1 (Drag and drop)
- **Axios**: 1.6.2 (HTTP client)
- **React Router**: 6.19.0 (Navigation)
- **Emotion**: Styling solution for MUI

### Project Structure
```
frontend/src/
├── components/
│   ├── KanbanBoard.js          # Main container component
│   ├── KanbanColumn.js         # Column container for cards
│   ├── LessonCard.js           # Individual card component
│   ├── WeeklyPlanHeader.js     # Header with user info and actions
│   ├── BoardFilters.js         # Advanced filtering interface
│   ├── BoardStatistics.js     # Analytics and metrics
│   └── LessonViewer.js         # Modal for viewing lesson details
├── App.js                      # Root component with theme
├── App.css                     # Global styles
├── index.js                    # Entry point
└── index.css                   # Base CSS reset
```

## Component Structure

### Component Hierarchy
```
App
└── KanbanBoard (Main Container)
    ├── WeeklyPlanHeader
    ├── BoardStatistics (conditional)
    ├── BoardFilters (conditional)
    ├── DragDropContext
    │   └── BoardContainer
    │       └── KanbanColumn (6 instances)
    │           └── LessonCard (multiple instances)
    ├── LessonViewer (modal)
    └── Notification Snackbar
```

## State Management

The application uses React hooks for state management without external libraries like Redux.

### Primary State (KanbanBoard.js)

#### Core Data State
```javascript
// Week plan data from API
const [weekPlan, setWeekPlan] = useState(null);

// Board data organized by columns
const [boardData, setBoardData] = useState({
  'monday': [],
  'tuesday': [],
  'wednesday': [],
  'thursday': [],
  'friday': [],
  'homework': []
});

// User profile information
const [userProfile, setUserProfile] = useState(null);
```

#### UI State
```javascript
// Loading and error states
const [loading, setLoading] = useState(true);
const [error, setError] = useState(null);
const [savingState, setSavingState] = useState(false);

// Filter and view states
const [showFilters, setShowFilters] = useState(false);
const [showAdvancedFilters, setShowAdvancedFilters] = useState(false);
const [showStatistics, setShowStatistics] = useState(false);
const [searchTerm, setSearchTerm] = useState('');

// Active filters configuration
const [activeFilters, setActiveFilters] = useState({
  subjects: [],
  days: [],
  sortBy: 'alphabetical',
  lessonCountRange: [0, 20],
  showEmptyColumns: true
});
```

#### Session Management
```javascript
// User session for persistence
const [userSession, setUserSession] = useState(null);

// Notification system
const [notification, setNotification] = useState({
  open: false,
  message: '',
  severity: 'info'
});
```

#### Lesson Viewer State
```javascript
// Modal state for lesson details
const [lessonViewerOpen, setLessonViewerOpen] = useState(false);
const [selectedLesson, setSelectedLesson] = useState(null);
```

### Computed State

#### Filtered and Sorted Data
```javascript
const filteredAndSortedBoardData = useMemo(() => {
  // Applies search, filters, and sorting to boardData
  // Returns processed data for each column
}, [boardData, searchTerm, activeFilters]);
```

## API Integration

### Base Configuration
- **Proxy**: `http://backend:8000` (configured in package.json)
- **Development URL**: `http://localhost:8001`

### Core Endpoints

#### User Profile
```javascript
GET /api/v1/user/profile
// Returns: { first_name: string, avatar_url: string }
```

#### Week Plan Data
```javascript
GET /api/v1/week-plan/latest?force_refresh=boolean
Headers: { 'user-session': sessionId }
// Returns: { data: weekPlanObject, saved_board_state?: object }
```

#### Session Management
```javascript
GET /api/v1/board-state/session
// Returns: { session_id: string }
```

#### Board State Persistence
```javascript
POST /api/v1/board-state/save
Headers: { 'user-session': sessionId }
Body: { board_data: object, weekly_plan_id: number }

DELETE /api/v1/board-state/clear
Headers: { 'user-session': sessionId }
Params: { weekly_plan_id: number }
```

### API Integration Pattern
```javascript
// Example API call with error handling
const fetchData = async () => {
  try {
    setLoading(true);
    const response = await axios.get('/api/endpoint', {
      headers: { 'user-session': userSession }
    });
    setData(response.data);
  } catch (error) {
    console.error('API Error:', error);
    setError('Failed to load data');
  } finally {
    setLoading(false);
  }
};
```

## Drag & Drop Implementation

### react-beautiful-dnd Setup

#### DragDropContext
```javascript
<DragDropContext onDragEnd={onDragEnd}>
  <BoardContainer>
    {columns.map(columnId => (
      <KanbanColumn key={columnId} columnId={columnId} />
    ))}
  </BoardContainer>
</DragDropContext>
```

#### Droppable Areas (Columns)
```javascript
<Droppable droppableId={columnId}>
  {(provided, snapshot) => (
    <div ref={provided.innerRef} {...provided.droppableProps}>
      {cards.map((card, index) => (
        <DraggableCard key={card.id} card={card} index={index} />
      ))}
      {provided.placeholder}
    </div>
  )}
</Droppable>
```

#### Draggable Items (Cards)
```javascript
<Draggable draggableId={card.id} index={index}>
  {(provided, snapshot) => (
    <div
      ref={provided.innerRef}
      {...provided.draggableProps}
      {...provided.dragHandleProps}
      style={{...provided.draggableProps.style}}
    >
      <CardContent />
    </div>
  )}
</Draggable>
```

### Drag End Handler Logic
```javascript
const onDragEnd = async (result) => {
  const { destination, source } = result;
  
  // Handle reordering within same column
  if (source.droppableId === destination.droppableId) {
    // Reorder logic
  } else {
    // Move between columns logic
    // Update board state
    // Save to backend
  }
};
```

## Styling & Theme

### Material-UI Theme Configuration
```javascript
const theme = createTheme({
  palette: {
    mode: 'light',
    primary: { main: '#673ab7' },
    secondary: { main: '#f50057' },
    background: {
      default: '#f4f5f7',
      paper: '#ffffff'
    }
  },
  typography: {
    fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
    h1: { fontWeight: 700, fontSize: '2.5rem' }
  },
  components: {
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: '12px',
          boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)'
        }
      }
    }
  }
});
```

### Styled Components Pattern
```javascript
const StyledComponent = styled(Component)(({ theme, customProp }) => ({
  // CSS properties
  backgroundColor: theme.palette.background.paper,
  padding: theme.spacing(2),
  // Conditional styling
  border: customProp ? '2px solid red' : 'none'
}));
```

### Color Scheme

#### Column Colors
- **Monday**: `#ff6b6b` (Red)
- **Tuesday**: `#4ecdc4` (Turquoise)
- **Wednesday**: `#45b7d1` (Blue)
- **Thursday**: `#96ceb4` (Green)
- **Friday**: `#ffeaa7` (Yellow)
- **Homework**: `#dda0dd` (Plum)

#### Subject Colors
- **Math/Maths**: `#FF6B6B`
- **English**: `#4ECDC4`
- **Science**: `#45B7D1`
- **Technology**: `#96CEB4`
- **Health**: `#FECA57`
- **PE**: `#FF9FF3`
- **History**: `#F8B500`
- **Geography**: `#98D8C8`

## Data Flow

### Data Transformation Pipeline

#### 1. Raw API Data → Cards
```javascript
const transformDataToCards = (weekPlanData) => {
  // Process classwork lessons
  // Process assignments
  // Create stable IDs
  // Distribute to columns
  // Return organized board data
};
```

#### 2. Card Structure
```javascript
const lessonCard = {
  id: 'lesson-{subjectIndex}-{lessonIndex}',
  type: 'lesson',
  subject: string,
  unit: string,
  topic: string,
  lesson: string,
  lessonNumber: string,
  days: array,
  notes: array,
  assignedDay: string,
  canvasLink: string,
  priority: 'low'|'medium'|'high',
  bookmarked: boolean
};

const assignmentCard = {
  id: 'assignment-{assignmentId}',
  type: 'assignment',
  subject: string,
  title: string,
  description: string,
  dueDate: string,
  canvasLink: string,
  assignedDay: 'homework',
  priority: 'high'
};
```

#### 3. Filtering & Sorting
```javascript
const applyFilters = (cards, filters) => {
  // Search term filtering
  // Subject filtering
  // Lesson count filtering
  // Bookmark filtering
  // Sorting (alphabetical, subject, lessonCount, recent)
};
```

### Persistence Flow
1. User action (drag/drop, bookmark)
2. Update local state
3. Save to localStorage (bookmarks)
4. Save to backend (board state)
5. Show confirmation notification

## Key Features

### 1. Personalized Welcome
- Fetches user profile from Canvas API
- Displays "Welcome, {firstName}!" with avatar
- Graceful fallback if profile unavailable

### 2. Advanced Filtering
- **Search**: Text search across subjects, topics, lessons
- **Subject Filter**: Multi-select subject filtering
- **Sorting**: Alphabetical, subject, lesson count, recent
- **Lesson Count Range**: Slider-based filtering
- **Empty Columns**: Toggle visibility of empty columns
- **Bookmarks**: Show only bookmarked items

### 3. Board Statistics
- **Overview Cards**: Total subjects, lessons, completion rate
- **Progress Breakdown**: Visual progress bars
- **Subject Analysis**: Top subjects by lesson count
- **Weekly Insights**: Scheduled days, notes, priority subjects

### 4. Lesson Viewer
- **Modal Interface**: Full-screen lesson details
- **Canvas Integration**: Direct links to Canvas content
- **Progress Tracking**: Mark as read/done
- **Bookmark Management**: Save important lessons

### 5. Session Persistence
- **Automatic Sessions**: UUID-based session management
- **Board State Saving**: Real-time state persistence
- **Bookmark Storage**: localStorage for bookmarks
- **Conflict Resolution**: Handle data mismatches

## Component API Reference

### KanbanBoard (Main Component)

#### State Management
```javascript
// Primary data
weekPlan: object | null
boardData: { [columnId]: Card[] }
userProfile: { first_name: string, avatar_url: string } | null

// UI state
loading: boolean
error: string | null
showFilters: boolean
showStatistics: boolean
searchTerm: string
activeFilters: FilterObject
```

#### Key Methods
```javascript
fetchWeekPlan(forceRefresh = false)
saveBoardState(boardData, sessionId)
onDragEnd(result)
handleFilterChange(newFilters)
handleViewLesson(lessonData)
```

### KanbanColumn

#### Props
```javascript
columnId: string          // 'monday', 'tuesday', etc.
title: string            // Display title with count
color: string            // Column theme color
cards: Card[]            // Filtered cards to display
totalCardCount: number   // Total cards (for count display)
onViewLesson: function   // Lesson click handler
hidden: boolean          // Visibility control
```

### LessonCard

#### Props
```javascript
card: Card              // Card data object
index: number           // Position in column
columnId: string        // Parent column ID
onViewLesson: function  // Click handler
```

#### Card Data Structure
```javascript
{
  id: string,
  type: 'lesson' | 'assignment',
  subject: string,
  unit?: string,
  topic?: string,
  lesson?: string,
  title?: string,
  assignedDay: string,
  priority: 'low' | 'medium' | 'high',
  bookmarked?: boolean,
  canvasLink: string
}
```

### WeeklyPlanHeader

#### Props
```javascript
weekPlan: object         // Week plan data
userProfile: object      // User profile data
onRefresh: function      // Refresh handler
onClearBoard: function   // Clear board handler
onForceRefresh: function // Force refresh handler
userSession: string      // Session ID
savingState: boolean     // Loading indicator
```

### BoardFilters

#### Props
```javascript
boardData: object        // Complete board data
onFilterChange: function // Filter change handler
onSearchChange: function // Search change handler
searchTerm: string       // Current search term
activeFilters: object    // Current filter state
showAdvanced: boolean    // Advanced filters visibility
onToggleAdvanced: function // Toggle advanced filters
```

### LessonViewer

#### Props
```javascript
open: boolean           // Modal visibility
onClose: function       // Close handler
card: Card             // Selected card data
onLessonUpdate: function // Progress update handler
onBookmarkChange: function // Bookmark handler
```

## Customization Guide

### 1. Changing the Color Scheme

#### Column Colors
```javascript
// In KanbanBoard.js
const getColumnColor = (columnId) => {
  switch (columnId) {
    case 'monday': return '#your-color';
    // ... other cases
  }
};
```

#### Subject Colors
```javascript
// In LessonCard.js or utilities
const getSubjectColor = (subject) => {
  const colorMap = {
    'Math': '#your-color',
    // ... other subjects
  };
  return colorMap[subject] || '#default-color';
};
```

### 2. Adding New Columns

#### 1. Update Initial State
```javascript
const initialBoardData = {
  'monday': [],
  'tuesday': [],
  'wednesday': [],
  'thursday': [],
  'friday': [],
  'homework': [],
  'your-new-column': []  // Add here
};
```

#### 2. Update Column Rendering
```javascript
['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'homework', 'your-new-column']
  .map((columnId) => (
    <KanbanColumn key={columnId} columnId={columnId} />
  ))
```

#### 3. Add Column Configuration
```javascript
const getColumnTitle = (columnId) => {
  const titles = {
    'your-new-column': 'Your Column Name'
  };
  // ... rest of function
};

const getColumnColor = (columnId) => {
  switch (columnId) {
    case 'your-new-column': return '#your-color';
    // ... other cases
  }
};
```

### 3. Customizing Card Layout

#### Card Structure
```javascript
// In LessonCard.js, modify the card content
<CardContent sx={{ p: 2 }}>
  {/* Your custom card layout */}
  <Typography variant="h6">{card.subject}</Typography>
  <Typography variant="body2">{card.lesson}</Typography>
  {/* Add your custom elements */}
</CardContent>
```

#### Adding Card Actions
```javascript
<CardActions>
  <IconButton onClick={handleCustomAction}>
    <CustomIcon />
  </IconButton>
</CardActions>
```

### 4. Adding New Filter Types

#### 1. Add to Filter State
```javascript
const [activeFilters, setActiveFilters] = useState({
  // ... existing filters
  yourNewFilter: defaultValue
});
```

#### 2. Update Filter Logic
```javascript
// In filteredAndSortedBoardData useMemo
if (activeFilters.yourNewFilter) {
  filtered = filtered.filter(card => {
    // Your filter logic
  });
}
```

#### 3. Add Filter UI
```javascript
// In BoardFilters.js
<FormControl fullWidth>
  <InputLabel>Your Filter</InputLabel>
  <Select
    value={activeFilters.yourNewFilter}
    onChange={handleYourFilterChange}
  >
    {/* Your filter options */}
  </Select>
</FormControl>
```

### 5. Theme Customization

#### Complete Theme Override
```javascript
const customTheme = createTheme({
  palette: {
    primary: { main: '#your-primary' },
    secondary: { main: '#your-secondary' },
    background: {
      default: '#your-background',
      paper: '#your-paper'
    }
  },
  typography: {
    fontFamily: '"Your Font", sans-serif'
  },
  components: {
    MuiCard: {
      styleOverrides: {
        root: {
          // Your card styles
        }
      }
    }
  }
});
```

### 6. Adding New Features

#### Feature Implementation Pattern
1. Add state for the feature
2. Create UI components
3. Implement event handlers
4. Add API integration (if needed)
5. Update persistence logic
6. Add to main component

#### Example: Adding a Priority Filter
```javascript
// 1. Add state
const [priorityFilter, setPriorityFilter] = useState('all');

// 2. Add filter logic
if (priorityFilter !== 'all') {
  filtered = filtered.filter(card => card.priority === priorityFilter);
}

// 3. Add UI
<Select value={priorityFilter} onChange={handlePriorityChange}>
  <MenuItem value="all">All Priorities</MenuItem>
  <MenuItem value="high">High</MenuItem>
  <MenuItem value="medium">Medium</MenuItem>
  <MenuItem value="low">Low</MenuItem>
</Select>
```

## Performance Considerations

### 1. useMemo for Expensive Computations
```javascript
const expensiveValue = useMemo(() => {
  // Expensive computation
}, [dependencies]);
```

### 2. useCallback for Event Handlers
```javascript
const handleEvent = useCallback((data) => {
  // Event handling logic
}, [dependencies]);
```

### 3. React.memo for Components
```javascript
const ExpensiveComponent = React.memo(({ prop1, prop2 }) => {
  // Component logic
}, (prevProps, nextProps) => {
  // Custom comparison
});
```

### 4. Virtual Scrolling (for large lists)
Consider implementing virtual scrolling for columns with many cards.

## Accessibility Features

### 1. Keyboard Navigation
- Tab navigation through cards and buttons
- Enter/Space for card interactions
- Escape to close modals

### 2. ARIA Labels
```javascript
<div
  role="button"
  aria-label="Open lesson details"
  tabIndex={0}
>
  {/* Card content */}
</div>
```

### 3. Screen Reader Support
- Meaningful text alternatives
- Proper heading hierarchy
- Status announcements

## Testing Strategy

### 1. Component Testing
```javascript
import { render, screen, fireEvent } from '@testing-library/react';
import KanbanBoard from './KanbanBoard';

test('renders board with columns', () => {
  render(<KanbanBoard />);
  expect(screen.getByText('Monday')).toBeInTheDocument();
});
```

### 2. Integration Testing
- API integration tests
- Drag and drop functionality
- State persistence

### 3. E2E Testing
- User workflows
- Cross-browser compatibility
- Performance testing

This documentation provides a comprehensive guide for understanding and modifying the ZSchool frontend while maintaining its core functionality. Use this as a reference for any UI/UX redesign work. 