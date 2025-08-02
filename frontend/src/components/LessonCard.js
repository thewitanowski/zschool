import React, { useState } from 'react';
import { Draggable } from 'react-beautiful-dnd';
import {
  Card,
  CardContent,
  Typography,
  Box,
  Collapse,
  IconButton,
  Divider,
  Avatar,
  LinearProgress,
  Tooltip,
  Badge
} from '@mui/material';
import { styled } from '@mui/material/styles';
import {
  ExpandMore as ExpandMoreIcon,
  School as SchoolIcon,
  CalendarToday as CalendarIcon,
  Notes as NotesIcon,
  Schedule as ScheduleIcon,
  Assignment as AssignmentIcon,
  PriorityHigh as PriorityHighIcon,
  CheckCircle as CheckCircleIcon,
  RadioButtonUnchecked as RadioButtonUncheckedIcon,
  MenuBook as ViewLessonIcon,
  Launch as LaunchIcon
} from '@mui/icons-material';

const StyledCard = styled(Card)(({ theme, assignedDay, subjectcolor }) => ({
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
    transform: 'translateY(-2px)',
    boxShadow: theme.shadows[4],
    cursor: 'grab'
  },
  '&:active': {
    cursor: 'grabbing'
  },
  opacity: assignedDay === 'homework' ? 0.85 : 1,
}));

const CardHeader = styled(Box)(({ theme }) => ({
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'space-between',
  marginBottom: theme.spacing(1),
}));

// Replace SubjectChip with SubjectTag
const SubjectTag = styled(Box)(({ theme, subject }) => ({
  display: 'inline-flex',
  alignItems: 'center',
  padding: '4px 12px',
  borderRadius: '16px',
  fontSize: '0.75rem',
  fontWeight: 600,
  color: 'white',
  backgroundColor: getSubjectColor(subject),
  textTransform: 'uppercase',
  letterSpacing: '0.5px',
}));

// Add SimpleTag component
const SimpleTag = styled(Box)(({ theme, bgcolor = '#e0e0e0', color = '#333' }) => ({
  display: 'inline-flex',
  alignItems: 'center',
  gap: '4px',
  padding: '2px 8px',
  borderRadius: '12px',
  fontSize: '0.7rem',
  fontWeight: 500,
  backgroundColor: bgcolor,
  color: color,
  border: '1px solid rgba(0,0,0,0.1)',
}));

const ExpandButton = styled(IconButton, {
  shouldForwardProp: (prop) => prop !== 'expanded'
})(({ expanded, theme }) => ({
  transform: expanded ? 'rotate(180deg)' : 'rotate(0deg)',
  transition: theme.transitions.create('transform', {
    duration: theme.transitions.duration.shortest,
  }),
  padding: theme.spacing(0.5),
}));

const ViewLessonButton = styled(IconButton)(({ theme }) => ({
  padding: theme.spacing(0.5),
  backgroundColor: 'rgba(103, 58, 183, 0.1)',
  color: theme.palette.secondary.main,
  '&:hover': {
    backgroundColor: 'rgba(103, 58, 183, 0.2)',
    transform: 'scale(1.1)',
  },
  transition: 'all 0.3s ease-in-out',
}));

const ProgressContainer = styled(Box)(({ theme }) => ({
  display: 'flex',
  alignItems: 'center',
  gap: theme.spacing(1),
  marginTop: theme.spacing(1),
}));

const MetadataRow = styled(Box)(({ theme }) => ({
  display: 'flex',
  alignItems: 'center',
  gap: theme.spacing(0.5),
  marginTop: theme.spacing(0.5),
  color: theme.palette.text.secondary,
  fontSize: '0.75rem',
}));

const ClickableArea = styled(Box)(({ theme }) => ({
  cursor: 'pointer',
  padding: theme.spacing(0.5),
  borderRadius: theme.spacing(0.5),
  transition: 'all 0.2s ease-in-out',
  '&:hover': {
    backgroundColor: 'rgba(0, 0, 0, 0.04)',
  },
}));

// Subject color mapping
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

// Get card priority (used for sorting and visual indicators)
const getCardPriority = (card) => {
  // Assignments are high priority
  if (card.type === 'assignment') return 'high';
  
  // High priority subjects or those with many lessons
  const highPrioritySubjects = ['Math', 'Maths', 'English', 'Science'];
  const isHighPriority = highPrioritySubjects.includes(card.subject);
  
  // Check if there's an explicit priority set
  if (card.priority) return card.priority;
  
  if (isHighPriority) return 'high';
  return 'medium';
};

// Calculate completion rate for progress indicator based on assigned day
const getCompletionEstimate = (assignedDay, lessons) => {
  switch (assignedDay) {
    case 'homework': return 100; // Completed work
    case 'friday': return 95; // End of week - almost complete
    case 'thursday': return 80; // Getting close to completion
    case 'wednesday': return 60; // Midweek progress
    case 'tuesday': return 40; // Early progress
    case 'monday': return 20; // Start of week
    default: return 0;
  }
};

const LessonCard = ({ card, index, columnId, onViewLesson }) => {
  const [expanded, setExpanded] = useState(false);
  
  const subjectColor = getSubjectColor(card.subject);
  const priority = getCardPriority(card);
  const completionRate = getCompletionEstimate(card.assignedDay, card.lessons);
  const hasNotes = card.notes && card.notes.length > 0;
  const hasDays = card.days && card.days.length > 0;
  const lessonCount = 1; // Each card represents one lesson now

  const handleExpandClick = (event) => {
    event.stopPropagation();
    setExpanded(!expanded);
  };

  const handleViewLesson = (event) => {
    event.stopPropagation();
    // Try to get a specific lesson number, defaulting to 1 if multiple lessons
    const lessonNumber = lessonCount > 0 ? 1 : Math.floor(Math.random() * 3) + 1;
    onViewLesson && onViewLesson({
      demoLessonNumber: lessonNumber,
      subject: card.subject,
      unit: card.unit,
      topic: card.topic
    });
  };

  const getPriorityIcon = () => {
    switch (priority) {
      case 'high':
        return <PriorityHighIcon sx={{ fontSize: 16, color: '#FF6B6B' }} />;
      case 'medium':
        return <PriorityHighIcon sx={{ fontSize: 16, color: '#FECA57' }} />;
      default:
        return null;
    }
  };

  const getStatusIcon = () => {
    switch (card.status) {
      case 'done':
        return <CheckCircleIcon sx={{ fontSize: 18, color: '#4CAF50' }} />;
      case 'in-progress':
        return <ScheduleIcon sx={{ fontSize: 18, color: '#FF9800' }} />;
      default:
        return <RadioButtonUncheckedIcon sx={{ fontSize: 18, color: '#9E9E9E' }} />;
    }
  };

  // Debug logging for drag issues
  console.log('🃏 Rendering card with ID:', card.id, 'at index:', index);
  
  return (
    <Draggable draggableId={card.id} index={index}>
      {(provided, snapshot) => (
        <StyledCard
          ref={provided.innerRef}
          {...provided.draggableProps}
          {...provided.dragHandleProps}
          subjectcolor={subjectColor}
          elevation={snapshot.isDragging ? 8 : 2}
        >
          <CardContent sx={{ p: 2, '&:last-child': { pb: 2 } }}>
            {/* Card Header */}
            <CardHeader>
              <Box display="flex" alignItems="center" gap={1}>
                <Avatar sx={{ 
                  width: 32, 
                  height: 32, 
                  backgroundColor: subjectColor,
                  fontSize: '0.8rem',
                  fontWeight: 'bold'
                }}>
                  {card.subject?.charAt(0)?.toUpperCase() || 'L'}
                </Avatar>
                
                <Box>
                  <SubjectTag 
                    subject={card.subject}
                  >
                    {card.subject}
                  </SubjectTag>
                  {priority !== 'low' && (
                    <Tooltip title={`${priority} priority`}>
                      <Badge badgeContent={getPriorityIcon()} sx={{ ml: 0.5 }}>
                        <Box />
                      </Badge>
                    </Tooltip>
                  )}
                </Box>
              </Box>

              <Box display="flex" alignItems="center" gap={0.5}>
                {getStatusIcon()}
                {card.canvasLink && (
                  <Tooltip title="Open in Canvas">
                    <ViewLessonButton 
                      onClick={(e) => {
                        e.stopPropagation();
                        window.open(card.canvasLink, '_blank');
                      }} 
                      size="small"
                    >
                      <LaunchIcon fontSize="small" />
                    </ViewLessonButton>
                  </Tooltip>
                )}
                <Tooltip title="View lesson content">
                  <ViewLessonButton onClick={handleViewLesson} size="small">
                    <ViewLessonIcon fontSize="small" />
                  </ViewLessonButton>
                </Tooltip>
                <ExpandButton 
                  expanded={expanded} 
                  onClick={handleExpandClick}
                  size="small"
                >
                  <ExpandMoreIcon fontSize="small" />
                </ExpandButton>
              </Box>
            </CardHeader>

            {/* Card Content - Now clickable */}
            <ClickableArea onClick={handleViewLesson}>
              <Box mb={1}>
                {/* Card Title based on type */}
                {card.type === 'assignment' ? (
                  <>
                    <Typography variant="h6" fontWeight={700} color="text.primary" sx={{ mb: 0.5 }}>
                      📋 {card.title}
                    </Typography>
                    {card.dueDate && (
                      <Typography variant="body2" fontWeight={600} color="error.main">
                        Due: {new Date(card.dueDate).toLocaleDateString()}
                      </Typography>
                    )}
                    {card.description && (
                      <Typography variant="body2" color="text.secondary" sx={{ 
                        display: '-webkit-box',
                        WebkitLineClamp: 2,
                        WebkitBoxOrient: 'vertical',
                        overflow: 'hidden'
                      }}>
                        {card.description}
                      </Typography>
                    )}
                  </>
                ) : (
                  <>
                    {/* Lesson Number/Name */}
                    <Typography variant="h6" fontWeight={700} color="text.primary" sx={{ mb: 0.5 }}>
                      📚 Lesson {card.lesson || card.lessonNumber}
                    </Typography>
                    
                    {card.unit && (
                      <Typography variant="body2" fontWeight={600} color="text.primary">
                        {card.unit}
                      </Typography>
                    )}
                    {card.topic && (
                      <Typography variant="body2" color="text.secondary">
                        {card.topic}
                      </Typography>
                    )}
                  </>
                )}
              </Box>
            </ClickableArea>

            {/* Quick Metadata */}
            <Box display="flex" flexWrap="wrap" gap={1} alignItems="center">
                              {lessonCount > 0 && (
                  <SimpleTag 
                    bgcolor="#E0F2F7" 
                    color="#1976D2" 
                    onClick={handleViewLesson}
                    sx={{ cursor: 'pointer', '&:hover': { opacity: 0.8 } }}
                  >
                    <AssignmentIcon sx={{ fontSize: '14px' }} />
                    {`${lessonCount} lesson${lessonCount !== 1 ? 's' : ''}`}
                  </SimpleTag>
                )}
              
                              {hasDays && (
                  <SimpleTag 
                    bgcolor="#E8F5E9" 
                    color="#2E7D32" 
                  >
                    <CalendarIcon sx={{ fontSize: '14px' }} />
                    {`${card.days.length} day${card.days.length !== 1 ? 's' : ''}`}
                  </SimpleTag>
                )}
              
                              {hasNotes && (
                  <SimpleTag 
                    bgcolor="#FFF3E0" 
                    color="#E65100" 
                  >
                    <NotesIcon sx={{ fontSize: '14px' }} />
                    Notes
                  </SimpleTag>
                )}
            </Box>

            {/* Removed fake progress indicator - percentages were misleading based on day of week */}

            {/* Expandable Details */}
            <Collapse in={expanded} timeout="auto" unmountOnExit>
              <Box mt={2}>
                <Divider sx={{ mb: 2 }} />
                
                {/* Canvas Link */}
                {card.canvasLink && (
                  <Box mb={2}>
                    <Typography variant="subtitle2" gutterBottom sx={{ 
                      display: 'flex', 
                      alignItems: 'center', 
                      gap: 0.5,
                      fontWeight: 600 
                    }}>
                      <LaunchIcon fontSize="small" />
                      Canvas Link
                    </Typography>
                    <SimpleTag 
                      onClick={(e) => {
                        e.stopPropagation();
                        window.open(card.canvasLink, '_blank');
                      }}
                      sx={{ 
                        cursor: 'pointer', 
                        '&:hover': { opacity: 0.8 },
                        color: 'primary.main',
                        borderColor: 'primary.main'
                      }}
                    >
                      Open in Canvas
                    </SimpleTag>
                  </Box>
                )}

                {/* Scheduled Days */}
                {hasDays && (
                  <Box mb={2}>
                    <Typography variant="subtitle2" gutterBottom sx={{ 
                      display: 'flex', 
                      alignItems: 'center', 
                      gap: 0.5,
                      fontWeight: 600 
                    }}>
                      <CalendarIcon fontSize="small" />
                      Scheduled Days
                    </Typography>
                                          <Box display="flex" flexWrap="wrap" gap={0.5}>
                        {card.days.map((day, idx) => (
                          <SimpleTag 
                            key={idx} 
                            bgcolor="#E3F2FD" 
                            color="#1976D2"
                          >
                            {day}
                          </SimpleTag>
                        ))}
                    </Box>
                  </Box>
                )}

                {/* Notes */}
                {hasNotes && (
                  <Box>
                    <Typography variant="subtitle2" gutterBottom sx={{ 
                      display: 'flex', 
                      alignItems: 'center', 
                      gap: 0.5,
                      fontWeight: 600 
                    }}>
                      <NotesIcon fontSize="small" />
                      Important Notes
                    </Typography>
                    {card.notes.map((note, idx) => (
                      <Typography 
                        key={idx} 
                        variant="body2" 
                        color="text.secondary"
                        sx={{ 
                          mb: 1,
                          p: 1,
                          backgroundColor: 'rgba(255, 193, 7, 0.1)',
                          borderRadius: 1,
                          borderLeft: '3px solid #FFC107'
                        }}
                      >
                        {note}
                      </Typography>
                    ))}
                  </Box>
                )}

                {/* Card Metadata */}
                <Box mt={2} pt={1} borderTop="1px solid rgba(0,0,0,0.1)">
                  <MetadataRow>
                    <Typography variant="caption" color="text.secondary">
                      Day: <strong style={{ textTransform: 'capitalize' }}>
                        {card.assignedDay || 'Unassigned'}
                      </strong>
                    </Typography>
                    {priority !== 'low' && (
                      <>
                        <Typography variant="caption">•</Typography>
                        <Typography variant="caption" color="text.secondary">
                          Priority: <strong style={{ color: priority === 'high' ? '#FF6B6B' : '#FECA57' }}>
                            {priority}
                          </strong>
                        </Typography>
                      </>
                    )}
                  </MetadataRow>
                  
                  {/* Click to view lesson hint */}
                  <Box mt={1}>
                    <Typography variant="caption" color="primary" sx={{ 
                      display: 'flex', 
                      alignItems: 'center', 
                      gap: 0.5,
                      cursor: 'pointer',
                      '&:hover': { textDecoration: 'underline' }
                    }} onClick={handleViewLesson}>
                      <ViewLessonIcon sx={{ fontSize: 12 }} />
                      Click to view lesson content
                    </Typography>
                  </Box>
                </Box>
              </Box>
            </Collapse>
          </CardContent>
        </StyledCard>
      )}
    </Draggable>
  );
};

export default LessonCard; 