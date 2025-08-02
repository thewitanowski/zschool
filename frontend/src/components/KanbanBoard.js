import React, { useState, useEffect, useMemo } from 'react';
import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd';
import axios from 'axios';
import {
  Box,
  Typography,
  Paper,
  Grid,
  CircularProgress,
  Alert,
  Card,
  CardContent,
  CardHeader,
  Divider,
  Container,
  Snackbar,
  Button,
  Tooltip,
  Fab
} from '@mui/material';
import { styled } from '@mui/material/styles';
import {
  FilterList as FilterIcon,
  Visibility as VisibilityIcon,
  VisibilityOff as VisibilityOffIcon,
  BarChart as BarChartIcon
} from '@mui/icons-material';

import LessonCard from './LessonCard';
import KanbanColumn from './KanbanColumn';
import WeeklyPlanHeader from './WeeklyPlanHeader';
import BoardFilters from './BoardFilters';
import BoardStatistics from './BoardStatistics';
import LessonViewer from './LessonViewer';

const StyledContainer = styled(Container)(({ theme }) => ({
  padding: theme.spacing(3),
  minHeight: '100vh',
  backgroundColor: '#f5f7fa',
}));

const BoardContainer = styled(Box)(({ theme }) => ({
  display: 'flex',
  gap: theme.spacing(3),
  overflowX: 'auto',
  minHeight: '70vh',
  padding: theme.spacing(2),
  borderRadius: theme.spacing(2),
  backgroundColor: 'rgba(255, 255, 255, 0.1)',
  backdropFilter: 'blur(10px)',
}));

const FilterToggleButton = styled(Button)(({ theme }) => ({
  position: 'fixed',
  bottom: theme.spacing(3),
  right: theme.spacing(3),
  zIndex: 1000,
  minWidth: 56,
  height: 56,
  borderRadius: '50%',
  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
  color: 'white',
  boxShadow: theme.shadows[8],
  '&:hover': {
    background: 'linear-gradient(135deg, #5a6fd8 0%, #6a3f8a 100%)',
    transform: 'scale(1.05)',
  },
}));

const StatsToggleButton = styled(Fab)(({ theme }) => ({
  position: 'fixed',
  bottom: theme.spacing(12),
  right: theme.spacing(3),
  zIndex: 1000,
  background: 'linear-gradient(135deg, #4ECDC4 0%, #44A08D 100%)',
  color: 'white',
  '&:hover': {
    background: 'linear-gradient(135deg, #3bb3b0 0%, #3a8b7a 100%)',
    transform: 'scale(1.05)',
  },
}));

const KanbanBoard = () => {
  const [weekPlan, setWeekPlan] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  // Initialize with all expected columns to prevent drag/drop errors
  const initialBoardData = {
    'monday': [],
    'tuesday': [],
    'wednesday': [],
    'thursday': [],
    'friday': [],
    'homework': []
  };
  
  const [boardData, setBoardData] = useState(initialBoardData);
  const [userSession, setUserSession] = useState(null);
  const [savingState, setSavingState] = useState(false);
  const [notification, setNotification] = useState({ open: false, message: '', severity: 'info' });
  
  // Advanced filtering state
  const [showFilters, setShowFilters] = useState(false);
  const [showAdvancedFilters, setShowAdvancedFilters] = useState(false);
  const [showStatistics, setShowStatistics] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [activeFilters, setActiveFilters] = useState({
    subjects: [],
    days: [],
    sortBy: 'alphabetical',
    lessonCountRange: [0, 20],
    showEmptyColumns: true
  });

  // Lesson viewer state
  const [lessonViewerOpen, setLessonViewerOpen] = useState(false);
  const [selectedLesson, setSelectedLesson] = useState(null);

  // Initialize session and fetch data
  useEffect(() => {
    initializeSession();
  }, []);

  const initializeSession = async () => {
    try {
      // Check if we have a session ID in localStorage
      let sessionId = localStorage.getItem('zschool_session_id');
      
      if (!sessionId) {
        // Generate new session ID
        const response = await axios.get('/api/v1/board-state/session');
        sessionId = response.data.session_id;
        localStorage.setItem('zschool_session_id', sessionId);
        console.log('Generated new session ID:', sessionId);
      } else {
        console.log('Using existing session ID:', sessionId);
      }
      
      setUserSession(sessionId);
      
      // Now fetch the week plan with session context
      await fetchWeekPlan(false, sessionId);
      
    } catch (err) {
      console.error('Failed to initialize session:', err);
      // Continue without session-based persistence
      await fetchWeekPlan();
    }
  };

  const fetchWeekPlan = async (forceRefresh = false, sessionId = userSession) => {
    try {
      setLoading(true);
      setError(null);
      
      // Set up headers with session ID if available
      const headers = sessionId ? { 'user-session': sessionId } : {};
      
      // Try to get real data first, fallback to mock data
      let response;
      try {
        response = await axios.get(`/api/v1/week-plan/latest?force_refresh=${forceRefresh}`, {
          headers
        });
      } catch (err) {
        console.warn('Failed to fetch real data, using mock data:', err);
        response = await axios.get('/api/v1/week-plan/mock');
      }
      
      const planData = response.data.data;
      setWeekPlan(planData);
      
      // Check if we have saved board state
      if (response.data.saved_board_state && sessionId) {
        console.log('Loading saved board state');
        
        // Transform fresh data first to get current card structure
        const freshData = transformDataToCards(planData);
        const savedData = response.data.saved_board_state.board_data;
        
        // Validate that saved card IDs still exist in fresh data
        const freshCardIds = new Set();
        Object.values(freshData).forEach(column => {
          column.forEach(card => freshCardIds.add(card.id));
        });
        
        const savedCardIds = new Set();
        Object.values(savedData).forEach(column => {
          column.forEach(card => savedCardIds.add(card.id));
        });
        
        // Check if saved IDs are still valid
        const savedIdsValid = Array.from(savedCardIds).every(id => freshCardIds.has(id));
        
        if (savedIdsValid) {
          setBoardData(savedData);
          showNotification('Loaded your saved progress!', 'success');
        } else {
          console.log('Saved board state has outdated card IDs, using fresh data');
          // Load bookmarks into fresh data
          const bookmarks = JSON.parse(localStorage.getItem('zschool_bookmarks') || '{}');
          Object.keys(freshData).forEach(columnId => {
            freshData[columnId] = freshData[columnId].map(card => ({
              ...card,
              bookmarked: !!bookmarks[card.id]
            }));
          });
          
          const completeData = { ...initialBoardData, ...freshData };
          setBoardData(completeData);
          showNotification('Data refreshed - previous layout reset', 'info');
        }
      } else {
        // Transform classwork into Kanban cards with default state
        const transformedData = transformDataToCards(planData);
        
        // Load bookmarks from localStorage
        const bookmarks = JSON.parse(localStorage.getItem('zschool_bookmarks') || '{}');
        Object.keys(transformedData).forEach(columnId => {
          transformedData[columnId] = transformedData[columnId].map(card => ({
            ...card,
            bookmarked: !!bookmarks[card.id]
          }));
        });
        
        // Ensure all columns exist in the transformed data
        const completeData = { ...initialBoardData, ...transformedData };
        setBoardData(completeData);
        
        if (sessionId && !response.data.saved_board_state) {
          // Save the initial state
          await saveBoardState(transformedData, sessionId, false);
        }
      }
      
    } catch (err) {
      console.error('Failed to fetch week plan:', err);
      setError('Failed to load weekly plan. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  // Helper function to assign cards to weekdays based on their days array
  const assignCardToDay = (days) => {
    if (!days || days.length === 0) return 'monday'; // Default to Monday if no days specified
    
    const dayMappings = {
      'monday': ['monday', 'mon', 'm'],
      'tuesday': ['tuesday', 'tue', 't'],
      'wednesday': ['wednesday', 'wed', 'w'],
      'thursday': ['thursday', 'thu', 'th'],
      'friday': ['friday', 'fri', 'f'],
      'homework': ['homework', 'hw', 'assignment', 'assignments']
    };
    
    // Check if any day in the array matches a weekday
    for (const [weekday, patterns] of Object.entries(dayMappings)) {
      for (const day of days) {
        if (patterns.some(pattern => day.toLowerCase().includes(pattern))) {
          return weekday;
        }
      }
    }
    
    // If it contains "homework" or similar, assign to homework
    const homeworkKeywords = ['homework', 'assignment', 'hw', 'study', 'review'];
    if (days.some(day => homeworkKeywords.some(keyword => day.toLowerCase().includes(keyword)))) {
      return 'homework';
    }
    
    // Default to Monday if no match found
    return 'monday';
  };

  // Intelligent lesson distribution based on assigned days and lesson count
  const distributeSubjectLessons = (subjectData) => {
    const lessons = subjectData.lessons || [];
    const assignedDays = subjectData.days || [];
    const lessonDistribution = [];
    
    console.log(`🎯 Distributing ${lessons.length} ${subjectData.subject} lessons across days:`, assignedDays);
    
    if (assignedDays.length === 0) {
      // No days assigned - distribute across weekdays
      const weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday'];
      lessons.forEach((lesson, index) => {
        const dayIndex = index % weekdays.length;
        lessonDistribution.push({
          lesson,
          assignedDay: weekdays[dayIndex]
        });
        console.log(`  📚 ${subjectData.subject} Lesson ${lesson} → ${weekdays[dayIndex]} (auto-distributed)`);
      });
    } else if (assignedDays.length === 1) {
      // Single day assigned - all lessons go to that day
      const targetDay = assignedDays[0].toLowerCase();
      const dayMap = {
        'monday': 'monday',
        'tuesday': 'tuesday', 
        'wednesday': 'wednesday',
        'thursday': 'thursday',
        'friday': 'friday'
      };
      const mappedDay = dayMap[targetDay] || 'homework';
      
      lessons.forEach((lesson) => {
        lessonDistribution.push({
          lesson,
          assignedDay: mappedDay
        });
        console.log(`  📚 ${subjectData.subject} Lesson ${lesson} → ${mappedDay} (single day assignment)`);
      });
    } else {
      // Multiple days assigned - distribute lessons evenly across them
      const dayMap = {
        'monday': 'monday',
        'tuesday': 'tuesday', 
        'wednesday': 'wednesday',
        'thursday': 'thursday',
        'friday': 'friday'
      };
      
      const mappedDays = assignedDays
        .map(day => dayMap[day.toLowerCase()])
        .filter(day => day); // Remove unmapped days
      
      if (mappedDays.length > 0) {
        lessons.forEach((lesson, index) => {
          const dayIndex = index % mappedDays.length;
          lessonDistribution.push({
            lesson,
            assignedDay: mappedDays[dayIndex]
          });
          console.log(`  📚 ${subjectData.subject} Lesson ${lesson} → ${mappedDays[dayIndex]} (multi-day distribution)`);
        });
      } else {
        // Fallback if no valid days mapped
        lessons.forEach((lesson) => {
          lessonDistribution.push({
            lesson,
            assignedDay: 'homework'
          });
        });
      }
    }
    
    return lessonDistribution;
  };

  const transformDataToCards = (weekPlanData) => {
    console.log('🔄 Transforming data to cards with lessons and assignments:', weekPlanData);
    const cards = [];
    
    // Process lessons from classwork
    const classwork = weekPlanData.classwork || [];
    classwork.forEach((item, subjectIndex) => {
      console.log(`📚 Processing ${item.subject} with ${item.lessons.length} lessons:`, item.lessons, 'Days:', item.days);
      
      // Get intelligent distribution for this subject
      const lessonDistribution = distributeSubjectLessons(item);
      
      lessonDistribution.forEach((lessonData, lessonIndex) => {
        // Get Canvas URL for this specific lesson
        const canvasUrls = item.canvas_urls || {};
        const specificCanvasUrl = canvasUrls[lessonData.lesson] || `https://learning.acc.edu.au/courses/20564/modules`;
        
        // Create stable ID based on subject and lesson number
        const stableId = `lesson-${item.subject.replace(/\s+/g, '-').toLowerCase()}-${lessonData.lesson}`;
        console.log('🆔 Generated card ID:', stableId, 'for lesson:', lessonData.lesson, 'subject:', item.subject);
        
        const card = {
          id: stableId,
          type: 'lesson',
          subject: item.subject,
          unit: item.unit,
          topic: item.topic,
          lesson: lessonData.lesson,
          lessonNumber: lessonData.lesson,
          days: item.days,
          notes: item.notes,
          assignedDay: lessonData.assignedDay,
          // Use specific Canvas URL for this lesson
          canvasLink: specificCanvasUrl,
          priority: 'medium' // Default priority
        };
        console.log(`  ➕ Created lesson card: ${item.subject} Lesson ${lessonData.lesson} → ${lessonData.assignedDay}`);
        console.log(`     🔗 Canvas URL: ${specificCanvasUrl}`);
        cards.push(card);
      });
    });

    // Process assignments - all go to homework column
    const assignments = weekPlanData.assignments || [];
    assignments.forEach((assignment, assignmentIndex) => {
      // Create stable ID based on assignment title and course
      const stableAssignmentId = `assignment-${assignment.course_id}-${assignment.title.replace(/\s+/g, '-').toLowerCase()}`;
      
      const assignmentCard = {
        id: stableAssignmentId,
        type: 'assignment',
        subject: assignment.context_name || 'Assignment',
        title: assignment.title || 'Untitled Assignment',
        description: assignment.description || '',
        dueDate: assignment.end_at || assignment.start_at,
        canvasLink: assignment.html_url || `https://learning.acc.edu.au/courses/${assignment.course_id}`,
        courseId: assignment.course_id,
        assignedDay: 'homework', // All assignments go to homework
        priority: 'high', // Assignments are typically high priority
        notes: []
      };
      console.log(`  📋 Created assignment card: ${assignmentCard.title} → homework`);
      console.log(`     🔗 Canvas URL: ${assignmentCard.canvasLink}`);
      cards.push(assignmentCard);
    });

    console.log(`✅ Total cards created: ${cards.length} (${cards.filter(c => c.type === 'lesson').length} lessons + ${cards.filter(c => c.type === 'assignment').length} assignments)`);

    // Distribute cards to appropriate weekday columns
    // Assignments go to homework, lessons stay in their assigned days
    const result = {
      'monday': cards.filter(card => card.assignedDay === 'monday'),
      'tuesday': cards.filter(card => card.assignedDay === 'tuesday'),
      'wednesday': cards.filter(card => card.assignedDay === 'wednesday'),
      'thursday': cards.filter(card => card.assignedDay === 'thursday'),
      'friday': cards.filter(card => card.assignedDay === 'friday'),
      'homework': cards.filter(card => card.type === 'assignment') // Only assignments in homework
    };

    console.log('📊 Cards distributed by day:', {
      monday: result.monday.length,
      tuesday: result.tuesday.length,
      wednesday: result.wednesday.length,
      thursday: result.thursday.length,
      friday: result.friday.length,
      homework: result.homework.length,
      total: cards.length
    });

    return result;
  };

  // Filtering and sorting logic
  const filteredAndSortedBoardData = useMemo(() => {
    const processCards = (cards) => {
      let filtered = [...cards];

      // TEMPORARILY DISABLE ALL FILTERING FOR DRAG AND DROP DEBUGGING
      console.log('🚨 Filtering temporarily disabled for drag debugging');
      return filtered; // Return all cards without filtering

      // Apply search filter
      if (searchTerm) {
        const term = searchTerm.toLowerCase();
        filtered = filtered.filter(card => 
          card.subject?.toLowerCase().includes(term) ||
          card.unit?.toLowerCase().includes(term) ||
          card.topic?.toLowerCase().includes(term) ||
          card.lesson?.toLowerCase().includes(term) ||
          card.notes?.some(note => note.toLowerCase().includes(term)) ||
          card.days?.some(day => day.toLowerCase().includes(term))
        );
      }

      // Apply subject filter
      if (activeFilters.subjects.length > 0) {
        filtered = filtered.filter(card => 
          activeFilters.subjects.includes(card.subject)
        );
      }

      // Apply lesson count filter - each card is now one lesson
      if (activeFilters.lessonCountRange) {
        const [min, max] = activeFilters.lessonCountRange;
        filtered = filtered.filter(card => {
          const lessonCount = 1; // Each card represents one lesson now
          return lessonCount >= min && (max >= 20 ? true : lessonCount <= max);
        });
      }

      // Apply bookmark filter
      if (activeFilters.bookmarked) {
        filtered = filtered.filter(card => card.bookmarked === true);
      }

      // Apply sorting
      switch (activeFilters.sortBy) {
        case 'subject':
          filtered.sort((a, b) => (a.subject || '').localeCompare(b.subject || ''));
          break;
        case 'lessonCount':
          filtered.sort((a, b) => a.lesson.localeCompare(b.lesson, undefined, { numeric: true }));
          break;
        case 'recent':
          // For now, maintain original order as "recent"
          break;
        case 'alphabetical':
        default:
          filtered.sort((a, b) => {
            const aText = `${a.subject || ''} ${a.unit || ''} ${a.topic || ''}`;
            const bText = `${b.subject || ''} ${b.unit || ''} ${b.topic || ''}`;
            return aText.localeCompare(bText);
          });
          break;
      }

      return filtered;
    };

    let result = {};
    
    // Ensure all expected columns exist
    const expectedColumns = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'homework'];
    
    expectedColumns.forEach(columnId => {
      if (activeFilters.days.length === 0 || activeFilters.days.includes(columnId)) {
        result[columnId] = processCards(boardData[columnId] || []);
      } else {
        result[columnId] = [];
      }
    });

    // Ensure all expected columns exist, even if empty
    const allColumns = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'homework'];
    allColumns.forEach(columnId => {
      if (!result[columnId]) {
        result[columnId] = [];
      }
    });

    return result;
  }, [boardData, searchTerm, activeFilters]);

  // Check if columns should be shown
  const shouldShowColumn = (columnId) => {
    if (!activeFilters.showEmptyColumns) {
      return (filteredAndSortedBoardData[columnId] || []).length > 0;
    }
    return true;
  };

  const saveBoardState = async (newBoardData = boardData, sessionId = userSession, showNotificationOnSave = true) => {
    if (!sessionId) {
      console.warn('No session ID available, skipping state save');
      return;
    }

    try {
      setSavingState(true);
      
      await axios.post('/api/v1/board-state/save', 
        {
          board_data: newBoardData,
          weekly_plan_id: 1 // Using default ID for mock data
        },
        {
          headers: { 'user-session': sessionId }
        }
      );
      
      if (showNotificationOnSave) {
        showNotification('Progress saved!', 'success');
      }
      
    } catch (err) {
      console.error('Failed to save board state:', err);
      showNotification('Failed to save progress', 'error');
    } finally {
      setSavingState(false);
    }
  };

  const onDragEnd = async (result) => {
    const { destination, source, draggableId } = result;
    
    console.log('🚀 Drag ended:', result);
    console.log('📦 Current boardData:', boardData);
    console.log('🔍 Looking for draggableId:', draggableId);
    
    // Check if the dragged card exists in any column
    let foundCard = null;
    let foundInColumn = null;
    Object.keys(boardData).forEach(columnId => {
      const card = boardData[columnId].find(c => c.id === draggableId);
      if (card) {
        foundCard = card;
        foundInColumn = columnId;
      }
    });
    
    console.log('🎯 Found card:', foundCard, 'in column:', foundInColumn);

    // If dropped outside a valid droppable area
    if (!destination) {
      console.log('❌ No destination - dropped outside valid area');
      return;
    }

    // If dropped in the same position
    if (
      destination.droppableId === source.droppableId &&
      destination.index === source.index
    ) {
      console.log('⏸️ Same position - no change needed');
      return;
    }

    // Use the card we already found from boardData search
    if (!foundCard) {
      console.log('❌ Could not find card with ID:', draggableId);
      console.log('📋 Available card IDs:');
      Object.keys(boardData).forEach(columnId => {
        console.log(`  ${columnId}:`, boardData[columnId].map(card => card.id));
      });
      return;
    }

    console.log('✅ Using found card:', foundCard, 'from column:', foundInColumn);

    // Update the card's assignedDay
    const updatedCard = {
      ...foundCard,
      assignedDay: destination.droppableId
    };

    // Create new board data by updating the card location
    const newBoardData = { ...boardData };
    
    // Remove the card from its current location in boardData
    newBoardData[foundInColumn] = newBoardData[foundInColumn].filter(card => card.id !== draggableId);
    
    // Add the updated card to the destination column in boardData
    newBoardData[destination.droppableId] = [...newBoardData[destination.droppableId], updatedCard];

    setBoardData(newBoardData);
    console.log('✅ Updated board data:', newBoardData);

    // Save the updated state to backend
    await saveBoardState(newBoardData);

    console.log(`Moved ${draggedCard.subject} from ${source.droppableId} to ${destination.droppableId}`);
  };

  const clearBoardState = async () => {
    if (!userSession) {
      console.warn('No session ID available, cannot clear state');
      return;
    }

    try {
      await axios.delete('/api/v1/board-state/clear', {
        headers: { 'user-session': userSession },
        params: { weekly_plan_id: 1 }
      });
      
      // Reset to default state
      if (weekPlan?.classwork) {
        const defaultData = transformDataToCards(weekPlan);
        setBoardData(defaultData);
        await saveBoardState(defaultData, userSession, false);
      }
      
      showNotification('Board reset to default state!', 'info');
      
    } catch (err) {
      console.error('Failed to clear board state:', err);
      showNotification('Failed to reset board', 'error');
    }
  };

  const showNotification = (message, severity = 'info') => {
    setNotification({ open: true, message, severity });
  };

  const forceClearAndRefresh = () => {
    console.log('🔄 Force clearing board state and refreshing...');
    localStorage.removeItem('zschool_bookmarks');
    fetchWeekPlan(true); // Force refresh
    showNotification('Force refreshed - all saved data cleared', 'info');
  };

  // Debug function to log all current card IDs
  const logAllCardIds = () => {
    console.log('📋 All current card IDs:');
    Object.keys(boardData).forEach(columnId => {
      console.log(`  ${columnId}:`, boardData[columnId].map(card => card.id));
    });
  };
  
  // Call this when board data changes
  React.useEffect(() => {
    logAllCardIds();
  }, [boardData]);

  const handleCloseNotification = () => {
    setNotification({ ...notification, open: false });
  };

  const getColumnTitle = (columnId) => {
    const count = filteredAndSortedBoardData[columnId]?.length || 0;
    const totalCount = boardData[columnId]?.length || 0;
    
    const titles = {
      'monday': 'Monday',
      'tuesday': 'Tuesday',
      'wednesday': 'Wednesday',
      'thursday': 'Thursday',
      'friday': 'Friday',
      'homework': 'Homework'
    };
    
    const filtered = count !== totalCount;
    return `${titles[columnId]} (${count}${filtered ? `/${totalCount}` : ''})`;
  };

  const getColumnColor = (columnId) => {
    switch (columnId) {
      case 'monday':
        return '#ff6b6b';  // Red
      case 'tuesday':
        return '#4ecdc4';  // Turquoise  
      case 'wednesday':
        return '#45b7d1';  // Blue
      case 'thursday':
        return '#96ceb4';  // Green
      case 'friday':
        return '#ffeaa7';  // Yellow
      case 'homework':
        return '#dda0dd';  // Plum
      default:
        return '#95a5a6';
    }
  };

  // Handle filter changes
  const handleFilterChange = (newFilters) => {
    setActiveFilters(newFilters);
  };

  const handleSearchChange = (term) => {
    setSearchTerm(term);
  };

  // Handle lesson viewing
  const handleViewLesson = (lessonData) => {
    setSelectedLesson(lessonData);
    setLessonViewerOpen(true);
    showNotification(`Opening lesson viewer for ${lessonData.subject}`, 'info');
  };

  const handleCloseLessonViewer = () => {
    setLessonViewerOpen(false);
    setSelectedLesson(null);
  };

  const handleBookmarkChange = (cardId, bookmarked) => {
    console.log('📌 Bookmark changed:', cardId, bookmarked);
    
    // Update the card in all columns
    const updatedBoardData = { ...boardData };
    Object.keys(updatedBoardData).forEach(columnId => {
      updatedBoardData[columnId] = updatedBoardData[columnId].map(card => 
        card.id === cardId ? { ...card, bookmarked } : card
      );
    });
    
    setBoardData(updatedBoardData);
    
    // Save to localStorage for persistence
    const bookmarks = JSON.parse(localStorage.getItem('zschool_bookmarks') || '{}');
    if (bookmarked) {
      bookmarks[cardId] = true;
    } else {
      delete bookmarks[cardId];
    }
    localStorage.setItem('zschool_bookmarks', JSON.stringify(bookmarks));
  };

  // Handle lesson status updates from the viewer
  const handleLessonUpdate = async (updateData) => {
    try {
      const { lessonId, action, completed, read } = updateData;
      
      if (action === 'mark-done' && completed) {
        // Find the card with this lesson and move it to 'homework' column (completed work)
        let updatedBoardData = { ...boardData };
        let cardToMove = null;
        let sourceColumn = null;
        
        // Search for the card in all columns
        Object.keys(updatedBoardData).forEach(columnId => {
          const cardIndex = updatedBoardData[columnId].findIndex(card => 
            card.subject && lessonId && card.subject.includes('demo') // For demo lessons
          );
          
          if (cardIndex !== -1) {
            cardToMove = updatedBoardData[columnId][cardIndex];
            sourceColumn = columnId;
          }
        });
        
        if (cardToMove && sourceColumn !== 'homework') {
          // Remove from source column
          updatedBoardData[sourceColumn] = updatedBoardData[sourceColumn].filter(
            card => card.id !== cardToMove.id
          );
          
          // Add to homework column (representing completed work)
          updatedBoardData['homework'] = [
            ...updatedBoardData['homework'],
            { ...cardToMove, completed: true }
          ];
          
          setBoardData(updatedBoardData);
          await saveBoardState(updatedBoardData, userSession, false);
          
          showNotification(`Lesson completed! Card moved to Homework column.`, 'success');
        }
      } else if (action === 'mark-read' && read) {
        // For read lessons, we could update the card appearance or metadata
        showNotification(`Lesson marked as read!`, 'info');
      }
      
    } catch (error) {
      console.error('Error handling lesson update:', error);
      showNotification('Failed to update board after lesson action', 'error');
    }
  };

  if (loading) {
    return (
      <StyledContainer>
        <Box display="flex" justifyContent="center" alignItems="center" minHeight="50vh">
          <CircularProgress size={60} />
          <Typography variant="h6" sx={{ ml: 2 }}>
            Loading your weekly plan...
          </Typography>
        </Box>
      </StyledContainer>
    );
  }

  if (error) {
    return (
      <StyledContainer>
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
        <Box display="flex" justifyContent="center">
          <button onClick={() => fetchWeekPlan()} style={{ padding: '10px 20px' }}>
            Try Again
          </button>
        </Box>
      </StyledContainer>
    );
  }

  return (
    <StyledContainer maxWidth={false}>
      {/* Weekly Plan Header */}
      {weekPlan && (
        <WeeklyPlanHeader 
          weekPlan={weekPlan} 
          onRefresh={() => fetchWeekPlan(true)}
          onClearBoard={clearBoardState}
          onForceRefresh={forceClearAndRefresh}
          userSession={userSession}
          savingState={savingState}
        />
      )}

      {/* Board Statistics */}
      {showStatistics && (
        <BoardStatistics
          boardData={boardData}
          filteredBoardData={filteredAndSortedBoardData}
          weekPlan={weekPlan}
        />
      )}

      {/* Board Filters */}
      {showFilters && (
        <BoardFilters
          boardData={boardData}
          onFilterChange={handleFilterChange}
          onSearchChange={handleSearchChange}
          searchTerm={searchTerm}
          activeFilters={activeFilters}
          showAdvanced={showAdvancedFilters}
          onToggleAdvanced={() => setShowAdvancedFilters(!showAdvancedFilters)}
        />
      )}

      {/* Kanban Board */}
      <DragDropContext 
        onDragEnd={onDragEnd}
        key={`drag-context-${Object.keys(boardData).map(k => boardData[k].length).join('-')}`}
      >
        <BoardContainer>
          {['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'homework']
            .map((columnId) => {
              const shouldShow = shouldShowColumn(columnId);
              return (
                <KanbanColumn
                  key={columnId}
                  columnId={columnId}
                  title={getColumnTitle(columnId)}
                  color={getColumnColor(columnId)}
                  cards={filteredAndSortedBoardData[columnId] || []}
                  cardCount={(filteredAndSortedBoardData[columnId] || []).length}
                  onViewLesson={handleViewLesson}
                  hidden={!shouldShow}
                />
              );
            })}
        </BoardContainer>
      </DragDropContext>

      {/* Week Summary */}
      {weekPlan && (
        <Box mt={4}>
          <Paper elevation={3} sx={{ p: 3, borderRadius: 2 }}>
            <Typography variant="h6" gutterBottom>
              Week Summary
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={12} md={3}>
                <Typography variant="body2" color="text.secondary">
                  Total Subjects: {weekPlan.classwork?.length || 0}
                </Typography>
              </Grid>
              <Grid item xs={12} md={3}>
                <Typography variant="body2" color="text.secondary">
                  Filtered Subjects: {Object.values(filteredAndSortedBoardData).flat().length}
                </Typography>
              </Grid>
              <Grid item xs={12} md={3}>
                <Typography variant="body2" color="text.secondary">
                  Teacher: {weekPlan.teacher?.name || 'Unknown'}
                </Typography>
              </Grid>
              <Grid item xs={12} md={3}>
                <Typography variant="body2" color="text.secondary">
                  Session: {userSession ? userSession.substring(0, 8) + '...' : 'No session'}
                </Typography>
              </Grid>
            </Grid>
          </Paper>
        </Box>
      )}

      {/* Statistics Toggle Button */}
      <StatsToggleButton
        onClick={() => setShowStatistics(!showStatistics)}
        size="medium"
      >
        <Tooltip title={showStatistics ? "Hide analytics" : "Show analytics"}>
          <BarChartIcon />
        </Tooltip>
      </StatsToggleButton>

      {/* Filter Toggle Button */}
      <FilterToggleButton
        onClick={() => setShowFilters(!showFilters)}
        variant="contained"
      >
        <Tooltip title={showFilters ? "Hide filters" : "Show filters"}>
          {showFilters ? <VisibilityOffIcon /> : <FilterIcon />}
        </Tooltip>
      </FilterToggleButton>

      {/* Lesson Viewer */}
      <LessonViewer
        open={lessonViewerOpen}
        onClose={handleCloseLessonViewer}
        card={selectedLesson}
        demoLessonNumber={selectedLesson?.demoLessonNumber}
        lessonId={selectedLesson?.lessonId}
        courseId={selectedLesson?.courseId}
        moduleItemId={selectedLesson?.moduleItemId}
        onLessonUpdate={handleLessonUpdate}
        onBookmarkChange={handleBookmarkChange}
      />

      {/* Notification Snackbar */}
      <Snackbar
        open={notification.open}
        autoHideDuration={3000}
        onClose={handleCloseNotification}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
      >
        <Alert 
          onClose={handleCloseNotification} 
          severity={notification.severity}
          sx={{ width: '100%' }}
        >
          {notification.message}
        </Alert>
      </Snackbar>
    </StyledContainer>
  );
};

export default KanbanBoard; 