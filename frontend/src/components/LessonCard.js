import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import { Draggable } from '@hello-pangea/dnd';
import {
  Card,
  CardContent,
  Typography,
  Box,
  Button,
  IconButton,
  Tooltip,
  Chip,
  Badge,
  Alert,
  CircularProgress
} from '@mui/material';
import { styled } from '@mui/material/styles';
import {
  DragIndicator as DragIcon,
  Assignment as AssignmentIcon,
  CheckCircle as DoneIcon,
  RadioButtonUnchecked as TodoIcon,
  Schedule as StartedIcon,
  Psychology as PsychologyIcon,
  Visibility as VisibilityIcon,
  AutoAwesome as ConvertIcon,
  Cached as CachedIcon,
  Bookmark as BookmarkIcon,
  BookmarkBorder as BookmarkBorderIcon,
  Launch as LaunchIcon
} from '@mui/icons-material';
import { useTheme } from '@mui/material/styles';

const StyledCard = styled(Card, {
  shouldForwardProp: (prop) => !['assignedDay', 'subjectcolor'].includes(prop)
})(({ theme, assignedDay, subjectcolor }) => ({
  marginBottom: theme.spacing(1),
  borderRadius: theme.spacing(1.5),
  cursor: 'grab',
  transition: 'all 0.3s ease-in-out',
  borderLeft: `4px solid ${subjectcolor || theme.palette.primary.main}`,
  background: assignedDay === 'homework' 
    ? 'linear-gradient(135deg, #e8f5e8 0%, #f1f8e9 100%)'
    : 'linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%)',
  boxShadow: theme.shadows[2],
  '&:hover': {
    // The transform property was interfering with react-beautiful-dnd positioning.
    // transform: 'translateY(-2px)', 
    boxShadow: theme.shadows[4],
    cursor: 'grab'
  },
  '&:active': {
    cursor: 'grabbing'
  },
  opacity: assignedDay === 'homework' ? 0.85 : 1,
}));

const SubjectChip = styled(Chip)(({ theme, subjectcolor }) => ({
  backgroundColor: subjectcolor,
  color: 'white',
  fontWeight: 600,
  fontSize: '0.75rem',
  height: '24px',
  maxWidth: '200px', // Limit maximum width
  '& .MuiChip-label': {
    paddingLeft: '8px',
    paddingRight: '8px',
    overflow: 'hidden',
    textOverflow: 'ellipsis',
    whiteSpace: 'nowrap',
    maxWidth: '100%',
  }
}));

const StatusChip = styled(Chip)(({ theme, status }) => {
  let backgroundColor, color, icon;
  
  switch (status) {
    case 'done':
      backgroundColor = '#4CAF50';
      color = 'white';
      break;
    case 'started':
    case 'in-progress':
      backgroundColor = '#FF9800';
      color = 'white';
      break;
    default: // 'todo'
      backgroundColor = '#9E9E9E';
      color = 'white';
      break;
  }
  
  return {
    backgroundColor,
    color,
    fontWeight: 500,
    fontSize: '0.7rem',
    height: '22px',
    '& .MuiChip-label': {
      paddingLeft: '6px',
      paddingRight: '6px',
    }
  };
});

const ActionButton = styled(Button)(({ theme, variant: buttonVariant }) => ({
  minWidth: 'auto',
  padding: '4px 8px',
  fontSize: '0.7rem',
  borderRadius: '6px',
  textTransform: 'none',
  ...(buttonVariant === 'canvas' && {
    backgroundColor: '#1976d2',
    color: 'white',
    '&:hover': {
      backgroundColor: '#1565c0',
    }
  }),
  ...(buttonVariant === 'convert' && {
    backgroundColor: '#9c27b0',
    color: 'white',
    '&:hover': {
      backgroundColor: '#7b1fa2',
    }
  }),
  ...(buttonVariant === 'view' && {
    backgroundColor: '#2e7d32',
    color: 'white',
    '&:hover': {
      backgroundColor: '#1b5e20',
    }
  })
}));

// Subject color mapping - preserving existing logic
const getSubjectColor = (subject) => {
  const colorMap = {
    'Math': '#FF6B6B',
    'Maths': '#FF6B6B',
    'English': '#4ECDC4',
    'Science': '#45B7D1',
    'Technology': '#96CEB4',
    'Health': '#FECA57',
    'PE': '#FF9FF3',
    'Physical Education': '#FF9FF3',
    'Spiritual and Physical Fitness': '#DDA0DD',
    'History': '#F8B500',
    'Geography': '#98D8C8',
    'Art': '#F06292',
    'Music': '#BA68C8',
    'Default': '#95A5A6'
  };
  
  return colorMap[subject] || colorMap['Default'];
};

const LessonCard = ({ card, index, columnId, onViewLesson }) => {
  const theme = useTheme();
  
  // Phase 1.4 Persistence: Enhanced state management
  const [isBookmarked, setIsBookmarked] = useState(false);
  const [isConverted, setIsConverted] = useState(false);
  const [isCheckingStatus, setIsCheckingStatus] = useState(false);
  const [conversionInfo, setConversionInfo] = useState(null);
  const [error, setError] = useState(null);

  // Generate cache key for localStorage
  const getCacheKey = useCallback(() => {
    if (card.courseId && card.lessonApiUrl) {
      const pageSlug = extractPageSlug(card);
      if (pageSlug) {
        return `conversion_${card.courseId}_${pageSlug}`;
      }
    }
    return `conversion_fallback_${card.subject}_${card.lesson}`;
  }, [card]);

  // Phase 1.4: Check conversion status on component mount
  useEffect(() => {
    checkConversionStatus();
  }, [card.courseId, card.lessonApiUrl]);

  const checkConversionStatus = async () => {
    try {
      setIsCheckingStatus(true);
      setError(null);

      // First check localStorage for quick response
      const cacheKey = getCacheKey();
      const cachedStatus = localStorage.getItem(cacheKey);
      if (cachedStatus) {
        const parsed = JSON.parse(cachedStatus);
        setIsConverted(parsed.isConverted);
        setConversionInfo(parsed.info);
      }

      // Then check with backend for authoritative status
      const pageSlug = extractPageSlug(card);
      if (pageSlug && card.courseId) {
        console.log('🔍 Checking conversion status:', { courseId: card.courseId, pageSlug });
        
        try {
          const response = await axios.get(
            `/api/v1/courses/${card.courseId}/pages/${pageSlug}/status`
          );
          
          const backendStatus = response.data;
          setIsConverted(backendStatus.is_converted);
          setConversionInfo(backendStatus);

          // Update localStorage with backend truth
          localStorage.setItem(cacheKey, JSON.stringify({
            isConverted: backendStatus.is_converted,
            info: backendStatus,
            lastChecked: new Date().toISOString()
          }));

          console.log('✅ Conversion status updated:', backendStatus);
        } catch (statusError) {
          // If status check fails, keep localStorage value or default to false
          console.warn('⚠️ Status check failed, using cached value:', statusError.message);
          if (!cachedStatus) {
            setIsConverted(false);
          }
        }
      } else {
        // For cards without proper course/page data, check localStorage only
        console.log('📝 No course/page data, using localStorage only');
      }
    } catch (error) {
      console.error('❌ Error checking conversion status:', error);
      setError('Failed to check conversion status');
      // Keep current state on error
    } finally {
      setIsCheckingStatus(false);
    }
  };

  // Phase 1.4: Updated handleConvertClick with persistence
  const handleConvertClick = async (event) => {
    event.stopPropagation();
    
    if (isConverted) {
      // If already converted, open the lesson viewer with AI conversion
      const pageSlug = extractPageSlug(card);
      if (pageSlug && card.courseId) {
        onViewLesson && onViewLesson({
          courseId: card.courseId,
          pageSlug: pageSlug,
          isAiConverted: true,
          subject: card.subject,
          unit: card.unit,
          topic: card.topic,
          title: card.topic || `${card.subject} - Lesson ${card.lesson}`
        });
      } else {
        // Fallback to demo lesson if no Canvas data available
        onViewLesson && onViewLesson({
          demoLessonNumber: card.lesson || card.lessonNumber || 1,
          subject: card.subject,
          unit: card.unit,
          topic: card.topic
        });
      }
    } else {
      // Phase 1.4: Trigger AI conversion
      const pageSlug = extractPageSlug(card);
      if (pageSlug && card.courseId) {
        console.log('🤖 Converting lesson with AI:', {
          courseId: card.courseId,
          pageSlug: pageSlug,
          lesson: card.lesson,
          subject: card.subject,
          canvasApiUrl: card.lessonApiUrl
        });
        
        // Update state optimistically
        setIsConverted(true);
        
        // Update localStorage immediately for responsive UX
        const cacheKey = getCacheKey();
        localStorage.setItem(cacheKey, JSON.stringify({
          isConverted: true,
          info: { status: 'converting', timestamp: new Date().toISOString() },
          lastChecked: new Date().toISOString()
        }));
        
        // Immediately open the lesson viewer with AI conversion
        onViewLesson && onViewLesson({
          courseId: card.courseId,
          pageSlug: pageSlug,
          isAiConverted: true,
          subject: card.subject,
          unit: card.unit,
          topic: card.topic,
          title: card.topic || `${card.subject} - Lesson ${card.lesson}`
        });
        
        // Background: verify conversion completed successfully
        setTimeout(async () => {
          try {
            await checkConversionStatus();
          } catch (error) {
            console.warn('Background status check failed:', error);
          }
        }, 2000);
        
      } else {
        console.warn('⚠️ Cannot convert lesson - missing courseId or pageSlug:', {
          courseId: card.courseId,
          pageSlug: pageSlug,
          lessonApiUrl: card.lessonApiUrl,
          cardData: card
        });
        
        // Fallback to setting as converted but show demo content
        setIsConverted(true);
        
        // Cache fallback conversion
        const cacheKey = getCacheKey();
        localStorage.setItem(cacheKey, JSON.stringify({
          isConverted: true,
          info: { status: 'fallback_demo', timestamp: new Date().toISOString() },
          lastChecked: new Date().toISOString()
        }));
        
        onViewLesson && onViewLesson({
          demoLessonNumber: card.lesson || card.lessonNumber || 1,
          subject: card.subject,
          unit: card.unit,
          topic: card.topic
        });
      }
    }
  };

  // Phase 1.4: Helper function to extract page_slug from card data
  const extractPageSlug = (card) => {
    // Try to extract page_slug from lessonApiUrl if available
    if (card.lessonApiUrl) {
      try {
        const url = new URL(card.lessonApiUrl);
        const pathParts = url.pathname.split('/');
        const pagesIndex = pathParts.indexOf('pages');
        if (pagesIndex !== -1 && pathParts[pagesIndex + 1]) {
          return pathParts[pagesIndex + 1];
        }
      } catch (e) {
        console.warn('Failed to parse lessonApiUrl:', card.lessonApiUrl);
      }
    }
    
    // Fallback: create page_slug from topic/title if available
    if (card.topic) {
      return card.topic
        .toLowerCase()
        .replace(/[^a-z0-9\s-]/g, '') // Remove special characters
        .replace(/\s+/g, '-') // Replace spaces with hyphens
        .replace(/-+/g, '-') // Replace multiple hyphens with single
        .trim();
    }
    
    // Last resort: use subject and lesson number
    if (card.subject && card.lesson) {
      return `${card.subject}-lesson-${card.lesson}`
        .toLowerCase()
        .replace(/[^a-z0-9\s-]/g, '')
        .replace(/\s+/g, '-')
        .replace(/-+/g, '-')
        .trim();
    }
    
    return null;
  };

  // Enhanced button display logic
  const getConvertButtonProps = () => {
    if (isCheckingStatus) {
      return {
        text: 'Checking...',
        icon: <CircularProgress size={16} />,
        color: 'default',
        disabled: true
      };
    }
    
    if (isConverted) {
      if (conversionInfo?.success === false) {
        return {
          text: 'Retry AI',
          icon: <ConvertIcon />,
          color: 'warning',
          disabled: false
        };
      }
      return {
        text: 'View Here',
        icon: conversionInfo?.cached ? <CachedIcon /> : <VisibilityIcon />,
        color: 'success',
        disabled: false
      };
    }
    
    return {
      text: 'Convert with AI',
      icon: <ConvertIcon />,
      color: 'primary',
      disabled: false
    };
  };

  const buttonProps = getConvertButtonProps();

  const subjectColor = getSubjectColor(card.subject);

  const handleBookmarkToggle = (event) => {
    event.stopPropagation();
    setIsBookmarked(!isBookmarked);
  };

  const handleCanvasClick = (event) => {
    event.stopPropagation();
    if (card.canvasLink) {
      window.open(card.canvasLink, '_blank');
    }
  };

  const getStatusDisplay = () => {
    switch (card.status) {
      case 'done':
        return { label: 'Done', status: 'done' };
      case 'started':
      case 'in-progress':
        return { label: 'Started', status: 'started' };
      default:
        return { label: 'To Do', status: 'todo' };
    }
  };

  const statusInfo = getStatusDisplay();

  // Debug logging for card rendering (only log if there might be an issue)
  if (!card.id || card.id.includes('undefined') || card.id.includes('null')) {
    console.error('🚨 LessonCard has invalid ID:', {
      cardId: card.id,
      index: index,
      columnId: columnId,
      subject: card.subject,
      lesson: card.lesson
    });
  }

  return (
    <Draggable draggableId={card.id} index={index}>
      {(provided, snapshot) => (
        <StyledCard
          ref={provided.innerRef}
          {...provided.draggableProps}
          subjectcolor={subjectColor}
          assignedDay={card.assignedDay}
          elevation={snapshot.isDragging ? 12 : 2}
          style={{
            ...provided.draggableProps.style,
            // When dragging, we apply some styles to make it stand out
            ...(snapshot.isDragging && {
              background: '#f8f9fa',
              boxShadow: theme.shadows[8],
              transform: `${provided.draggableProps.style?.transform || ''} rotate(3deg)`,
            })
          }}
        >
          <CardContent sx={{ p: 2, '&:last-child': { pb: 2 } }}>
            {/* Top Row: Subject and Status Chips */}
            <Box display="flex" justifyContent="space-between" alignItems="flex-start" mb={1}>
              <Box display="flex" gap={1} alignItems="center">
                <SubjectChip 
                  label={card.subject}
                  size="small"
                  subjectcolor={subjectColor}
                />
                <StatusChip 
                  label={statusInfo.label}
                  size="small"
                  status={statusInfo.status}
                />
              </Box>
              
              {/* Top Right: Bookmark and Drag Handle */}
              <Box display="flex" alignItems="center" gap={0.5}>
                <Tooltip title={isBookmarked ? "Remove bookmark" : "Bookmark lesson"}>
                  <IconButton 
                    size="small" 
                    onClick={handleBookmarkToggle}
                    sx={{ p: 0.5 }}
                  >
                    {isBookmarked ? 
                      <BookmarkIcon sx={{ fontSize: 18, color: '#ff9800' }} /> : 
                      <BookmarkBorderIcon sx={{ fontSize: 18, color: '#9e9e9e' }} />
                    }
                  </IconButton>
                </Tooltip>
                <Box {...provided.dragHandleProps}>
                  <DragIcon sx={{ fontSize: 18, color: '#9e9e9e', cursor: 'grab' }} />
                </Box>
              </Box>
            </Box>

            {/* Lesson Name - preserving existing logic */}
            <Typography variant="h6" fontWeight={600} color="text.primary" sx={{ mb: 0.5 }}>
              {card.type === 'assignment' ? (
                <>📋 {card.title}</>
              ) : (
                <>📚 Lesson {card.lesson || card.lessonNumber}</>
              )}
            </Typography>

            {/* Topic/Unit - preserving existing logic */}
            <Box mb={2}>
              {card.unit && (
                <Typography variant="body2" fontWeight={500} color="text.primary" sx={{ mb: 0.25 }}>
                  {card.unit}
                </Typography>
              )}
              {card.topic && (
                <Typography variant="body2" color="text.secondary">
                  {card.topic}
                </Typography>
              )}
            </Box>

            {/* Action Buttons */}
            <Box display="flex" gap={1}>
              {card.canvasLink && (
                <ActionButton
                  variant="canvas"
                  onClick={handleCanvasClick}
                  startIcon={<LaunchIcon sx={{ fontSize: 14 }} />}
                  size="small"
                >
                  Canvas
                </ActionButton>
              )}
              <ActionButton
                variant={buttonProps.color === 'success' ? "view" : "convert"}
                onClick={handleConvertClick}
                startIcon={buttonProps.icon}
                size="small"
                disabled={buttonProps.disabled}
                color={buttonProps.color}
              >
                {buttonProps.text}
              </ActionButton>
            </Box>
          </CardContent>
        </StyledCard>
      )}
    </Draggable>
  );
};

export default LessonCard; 