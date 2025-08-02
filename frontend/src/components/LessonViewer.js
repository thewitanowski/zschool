import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Box,
  Typography,
  Paper,
  Button,
  IconButton,
  Divider,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Card,
  CardContent,
  CardHeader,
  LinearProgress,
  Alert,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  CircularProgress,
  Skeleton,
  ButtonGroup
} from '@mui/material';
import { styled } from '@mui/material/styles';
import {
  Close as CloseIcon,
  CheckCircle as CheckCircleIcon,
  Schedule as ScheduleIcon,
  School as SchoolIcon,
  Assignment as AssignmentIcon,
  Psychology as PsychologyIcon,
  Lightbulb as LightbulbIcon,
  Link as LinkIcon,
  VideoLibrary as VideoIcon,
  PictureAsPdf as FileIcon,
  ExpandMore as ExpandMoreIcon,
  Launch as LaunchIcon,
  BookmarkBorder as BookmarkIcon,
  Bookmark as BookmarkedIcon,
  TaskAlt as MarkDoneIcon,
  Visibility as MarkReadIcon,
  Sync as SyncIcon,
  Check as CheckIcon
} from '@mui/icons-material';

const StyledDialog = styled(Dialog)(({ theme }) => ({
  '& .MuiDialog-paper': {
    minHeight: '80vh',
    maxHeight: '90vh',
    width: '90vw',
    maxWidth: '1000px',
    borderRadius: theme.spacing(2),
    background: 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)',
  },
}));

const StyledDialogTitle = styled(DialogTitle)(({ theme }) => ({
  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
  color: 'white',
  padding: theme.spacing(3),
  position: 'relative',
  '& .MuiTypography-root': {
    fontWeight: 600,
    fontSize: '1.5rem',
  },
}));

const ContentContainer = styled(Box)(({ theme }) => ({
  padding: theme.spacing(3),
  maxHeight: '60vh',
  overflowY: 'auto',
  '&::-webkit-scrollbar': {
    width: '8px',
  },
  '&::-webkit-scrollbar-track': {
    background: 'rgba(0,0,0,0.1)',
    borderRadius: '4px',
  },
  '&::-webkit-scrollbar-thumb': {
    background: 'rgba(0,0,0,0.3)',
    borderRadius: '4px',
    '&:hover': {
      background: 'rgba(0,0,0,0.5)',
    },
  },
}));

const SummaryCard = styled(Card)(({ theme }) => ({
  marginBottom: theme.spacing(3),
  background: 'rgba(255, 255, 255, 0.9)',
  backdropFilter: 'blur(10px)',
  borderRadius: theme.spacing(2),
  border: '1px solid rgba(255, 255, 255, 0.2)',
}));

const SectionCard = styled(Card)(({ theme }) => ({
  marginBottom: theme.spacing(2),
  background: 'rgba(255, 255, 255, 0.7)',
  backdropFilter: 'blur(5px)',
  borderRadius: theme.spacing(1.5),
  transition: 'all 0.3s ease-in-out',
  '&:hover': {
    transform: 'translateY(-2px)',
    boxShadow: theme.shadows[8],
    background: 'rgba(255, 255, 255, 0.9)',
  },
}));

const MetadataChip = styled(Box)(({ theme, variant = 'default' }) => ({
  display: 'inline-flex',
  alignItems: 'center',
  gap: '4px',
  padding: '4px 8px',
  borderRadius: '12px',
  fontSize: '0.75rem',
  fontWeight: 500,
  margin: theme.spacing(0.5),
  border: '1px solid rgba(0,0,0,0.1)',
  ...(variant === 'time' && {
    backgroundColor: 'rgba(76, 175, 80, 0.2)',
    color: '#2E7D32',
  }),
  ...(variant === 'type' && {
    backgroundColor: 'rgba(33, 150, 243, 0.2)',
    color: '#1976D2',
  }),
  ...(variant === 'default' && {
    backgroundColor: 'rgba(255, 255, 255, 0.8)',
    color: '#333',
  }),
}));

const ObjectivesList = styled(List)(({ theme }) => ({
  padding: 0,
  '& .MuiListItem-root': {
    paddingLeft: 0,
    paddingRight: 0,
  },
}));

const ResourceCard = styled(Card)(({ theme }) => ({
  marginTop: theme.spacing(1),
  marginBottom: theme.spacing(1),
  backgroundColor: 'rgba(255, 193, 7, 0.1)',
  border: '1px solid rgba(255, 193, 7, 0.3)',
  cursor: 'pointer',
  transition: 'all 0.3s ease-in-out',
  '&:hover': {
    backgroundColor: 'rgba(255, 193, 7, 0.2)',
    transform: 'translateX(4px)',
  },
}));

const LoadingContainer = styled(Box)(({ theme }) => ({
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  justifyContent: 'center',
  padding: theme.spacing(4),
  minHeight: '300px',
}));

const ActionButtonGroup = styled(ButtonGroup)(({ theme }) => ({
  boxShadow: theme.shadows[3],
  '& .MuiButton-root': {
    borderColor: 'rgba(255, 255, 255, 0.3)',
    '&:hover': {
      borderColor: 'rgba(255, 255, 255, 0.5)',
      backgroundColor: 'rgba(255, 255, 255, 0.1)',
    },
  },
}));

const StatusIndicator = styled(Box)(({ theme, status }) => ({
  display: 'flex',
  alignItems: 'center',
  gap: theme.spacing(1),
  padding: theme.spacing(1, 2),
  borderRadius: theme.spacing(1),
  backgroundColor: 
    status === 'done' ? 'rgba(76, 175, 80, 0.1)' :
    status === 'read' ? 'rgba(33, 150, 243, 0.1)' :
    'rgba(158, 158, 158, 0.1)',
  color:
    status === 'done' ? theme.palette.success.main :
    status === 'read' ? theme.palette.primary.main :
    theme.palette.text.secondary,
  fontSize: '0.875rem',
  fontWeight: 500,
}));

const LessonViewer = ({ 
  open, 
  onClose, 
  card = null,
  lessonId = null, 
  courseId = null, 
  moduleItemId = null,
  demoLessonNumber = null,
  onLessonUpdate = null, // Callback for when lesson status changes
  onBookmarkChange = null // Callback for when bookmark status changes
}) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [lessonContent, setLessonContent] = useState(null);
  const [bookmarked, setBookmarked] = useState(card?.bookmarked || false);
  const [completed, setCompleted] = useState(false);
  const [read, setRead] = useState(false);
  const [actionLoading, setActionLoading] = useState('');
  const [canvasStatus, setCanvasStatus] = useState(null);
  const [notification, setNotification] = useState({ open: false, message: '', severity: 'info' });

  // Fetch lesson content when dialog opens
  useEffect(() => {
    if (open && (lessonId || (courseId && moduleItemId) || demoLessonNumber)) {
      fetchLessonContent();
    }
  }, [open, lessonId, courseId, moduleItemId, demoLessonNumber]);

  const fetchLessonContent = async () => {
    try {
      setLoading(true);
      setError(null);
      
      let response;
      
      if (demoLessonNumber) {
        // Fetch demo lesson content
        response = await axios.get(`/api/v1/lessons/demo/${demoLessonNumber}`);
      } else if (lessonId) {
        // Fetch by lesson ID with Canvas status
        try {
          response = await axios.get(`/api/v1/lessons/${lessonId}/canvas-status`);
          setCanvasStatus(response.data.canvas_status);
        } catch (err) {
          // Fallback to regular lesson content
          response = await axios.get(`/api/v1/lessons/${lessonId}`);
        }
      } else if (courseId && moduleItemId) {
        // Fetch from Canvas
        response = await axios.get(`/api/v1/lessons/canvas/${courseId}/${moduleItemId}`);
      }
      
      if (response?.data?.data) {
        setLessonContent(response.data.data);
        
        // Set status based on Canvas or lesson data
        if (response.data.canvas_status) {
          setCompleted(response.data.canvas_status.completed || false);
        } else {
          setCompleted(false);
        }
        
        setBookmarked(false); // Placeholder
        setRead(false); // Placeholder
      } else {
        throw new Error('No lesson content received');
      }
      
    } catch (err) {
      console.error('Failed to fetch lesson content:', err);
      setError(err.response?.data?.detail || err.message || 'Failed to load lesson content');
    } finally {
      setLoading(false);
    }
  };

  const handleMarkAsDone = async () => {
    if (!lessonId || demoLessonNumber) {
      showNotification('Mark as Done is only available for real Canvas lessons', 'warning');
      return;
    }
    
    try {
      setActionLoading('done');
      const userSession = localStorage.getItem('zschool_session_id');
      
      if (!userSession) {
        showNotification('No session found. Please refresh the page.', 'error');
        return;
      }
      
      // Use demo course/module IDs for testing
      const testCourseId = courseId || 20564;
      const testModuleItemId = moduleItemId || 12345;
      
      const response = await axios.post(
        `/api/v1/lessons/${lessonId}/mark-done`,
        {
          course_id: testCourseId,
          module_item_id: testModuleItemId
        },
        {
          headers: { 'user-session': userSession }
        }
      );
      
      if (response.data.status === 'success') {
        setCompleted(true);
        showNotification('Lesson marked as done!', 'success');
        
        // Trigger board update callback
        if (onLessonUpdate) {
          onLessonUpdate({
            lessonId,
            action: 'mark-done',
            completed: true
          });
        }
      }
      
    } catch (err) {
      console.error('Failed to mark lesson as done:', err);
      showNotification(
        err.response?.data?.detail || 'Failed to mark lesson as done',
        'error'
      );
    } finally {
      setActionLoading('');
    }
  };

  const handleMarkAsRead = async () => {
    try {
      setActionLoading('read');
      const userSession = localStorage.getItem('zschool_session_id');
      
      if (!userSession) {
        showNotification('No session found. Please refresh the page.', 'error');
        return;
      }
      
      let response;
      
      if (demoLessonNumber) {
        // For demo lessons, just update local state
        setRead(true);
        showNotification('Demo lesson marked as read!', 'success');
        return;
      }
      
      if (lessonId) {
        response = await axios.post(
          `/api/v1/lessons/${lessonId}/mark-read`,
          {},
          {
            headers: { 'user-session': userSession }
          }
        );
        
        if (response.data.status === 'success') {
          setRead(true);
          showNotification('Lesson marked as read!', 'success');
          
          // Trigger board update callback
          if (onLessonUpdate) {
            onLessonUpdate({
              lessonId,
              action: 'mark-read',
              read: true
            });
          }
        }
      }
      
    } catch (err) {
      console.error('Failed to mark lesson as read:', err);
      showNotification(
        err.response?.data?.detail || 'Failed to mark lesson as read',
        'error'
      );
    } finally {
      setActionLoading('');
    }
  };

  const handleSyncWithCanvas = async () => {
    if (!lessonId || demoLessonNumber) {
      showNotification('Canvas sync is only available for real Canvas lessons', 'warning');
      return;
    }
    
    try {
      setActionLoading('sync');
      
      // Refresh lesson with Canvas status
      const response = await axios.get(`/api/v1/lessons/${lessonId}/canvas-status`);
      
      if (response.data.status === 'success') {
        setCanvasStatus(response.data.canvas_status);
        if (response.data.canvas_status?.completed !== undefined) {
          setCompleted(response.data.canvas_status.completed);
        }
        showNotification('Synced with Canvas successfully!', 'success');
      }
      
    } catch (err) {
      console.error('Failed to sync with Canvas:', err);
      showNotification('Failed to sync with Canvas', 'error');
    } finally {
      setActionLoading('');
    }
  };

  const handleBookmark = () => {
    const newBookmarked = !bookmarked;
    setBookmarked(newBookmarked);
    
    // Update the card's bookmark status
    if (onBookmarkChange) {
      onBookmarkChange(card.id, newBookmarked);
    }
    
    showNotification(
      bookmarked ? 'Bookmark removed' : 'Lesson bookmarked!',
      'info'
    );
  };

  const showNotification = (message, severity = 'info') => {
    setNotification({ open: true, message, severity });
    setTimeout(() => {
      setNotification({ open: false, message: '', severity: 'info' });
    }, 3000);
  };

  const renderSection = (section, index) => {
    const getIcon = (type) => {
      switch (type) {
        case 'video': return <VideoIcon />;
        case 'image': return <LinkIcon />;
        case 'code': return <AssignmentIcon />;
        case 'list': return <LightbulbIcon />;
        default: return <SchoolIcon />;
      }
    };

    return (
      <SectionCard key={index} elevation={2}>
        <CardHeader
          avatar={getIcon(section.type)}
          title={section.heading}
          titleTypographyProps={{ 
            variant: 'h6', 
            fontWeight: 600,
            color: 'primary.main'
          }}
        />
        <CardContent sx={{ pt: 0 }}>
          <Typography 
            variant="body1" 
            sx={{ 
              whiteSpace: 'pre-wrap', 
              lineHeight: 1.6,
              color: 'text.primary'
            }}
          >
            {section.content}
          </Typography>
        </CardContent>
      </SectionCard>
    );
  };

  const renderResource = (resource, index) => {
    const getResourceIcon = (type) => {
      switch (type) {
        case 'video': return <VideoIcon color="primary" />;
        case 'file': return <FileIcon color="secondary" />;
        case 'link': return <LinkIcon color="action" />;
        default: return <LaunchIcon color="action" />;
      }
    };

    return (
      <ResourceCard 
        key={index}
        onClick={() => window.open(resource.url, '_blank')}
        elevation={1}
      >
        <CardContent sx={{ display: 'flex', alignItems: 'center', p: 2, '&:last-child': { pb: 2 } }}>
          {getResourceIcon(resource.type)}
          <Box sx={{ ml: 2, flexGrow: 1 }}>
            <Typography variant="body2" fontWeight={600}>
              {resource.title}
            </Typography>
            <Typography variant="caption" color="text.secondary">
              {resource.type} • Click to open
            </Typography>
          </Box>
          <LaunchIcon sx={{ color: 'text.secondary' }} />
        </CardContent>
      </ResourceCard>
    );
  };

  const renderLoadingState = () => (
    <LoadingContainer>
      <CircularProgress size={60} sx={{ mb: 2 }} />
      <Typography variant="h6" color="text.secondary">
        Loading lesson content...
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
        Transforming content for optimal learning
      </Typography>
    </LoadingContainer>
  );

  const renderErrorState = () => (
    <Box sx={{ p: 3 }}>
      <Alert 
        severity="error" 
        sx={{ mb: 2 }}
        action={
          <Button color="inherit" size="small" onClick={fetchLessonContent}>
            Retry
          </Button>
        }
      >
        {error}
      </Alert>
      <Typography variant="body2" color="text.secondary">
        Unable to load lesson content. This may be due to network issues or the content may not be available.
      </Typography>
    </Box>
  );

  const getLessonStatus = () => {
    if (completed) return 'done';
    if (read) return 'read';
    return 'not-started';
  };

  const getStatusText = () => {
    if (completed) return 'Completed';
    if (read) return 'Read';
    return 'Not Started';
  };

  const getStatusIcon = () => {
    if (completed) return <CheckCircleIcon />;
    if (read) return <MarkReadIcon />;
    return <ScheduleIcon />;
  };

  return (
    <>
      <StyledDialog
        open={open}
        onClose={onClose}
        maxWidth={false}
        scroll="body"
      >
        <StyledDialogTitle>
          <Box display="flex" justifyContent="space-between" alignItems="center">
            <Box>
              <Typography variant="h5">
                {loading ? 'Loading Lesson...' : lessonContent?.title || 'Lesson Content'}
              </Typography>
              {lessonContent?.type && (
                <Box display="flex" alignItems="center" gap={2} sx={{ mt: 0.5 }}>
                  <Typography variant="subtitle1" sx={{ opacity: 0.9 }}>
                    {lessonContent.type} • {lessonContent.estimated_time || '5-10 minutes'}
                  </Typography>
                  <StatusIndicator status={getLessonStatus()}>
                    {getStatusIcon()}
                    {getStatusText()}
                  </StatusIndicator>
                </Box>
              )}
            </Box>
            <Box display="flex" alignItems="center" gap={1}>
              {lessonContent && (
                <>
                  <ActionButtonGroup variant="contained" color="primary">
                    <Button
                      onClick={handleMarkAsRead}
                      disabled={actionLoading === 'read' || read}
                      startIcon={
                        actionLoading === 'read' ? 
                        <CircularProgress size={16} /> : 
                        read ? <CheckIcon /> : <MarkReadIcon />
                      }
                      size="small"
                    >
                      {read ? 'Read' : 'Mark Read'}
                    </Button>
                    
                    <Button
                      onClick={handleMarkAsDone}
                      disabled={actionLoading === 'done' || completed || demoLessonNumber}
                      startIcon={
                        actionLoading === 'done' ? 
                        <CircularProgress size={16} /> : 
                        completed ? <CheckIcon /> : <MarkDoneIcon />
                      }
                      size="small"
                      color={completed ? 'success' : 'primary'}
                    >
                      {completed ? 'Done' : 'Mark Done'}
                    </Button>
                    
                    {lessonId && !demoLessonNumber && (
                      <Button
                        onClick={handleSyncWithCanvas}
                        disabled={actionLoading === 'sync'}
                        startIcon={
                          actionLoading === 'sync' ? 
                          <CircularProgress size={16} /> : 
                          <SyncIcon />
                        }
                        size="small"
                      >
                        Sync
                      </Button>
                    )}
                  </ActionButtonGroup>
                  
                  <IconButton 
                    onClick={handleBookmark}
                    sx={{ color: 'white' }}
                    title={bookmarked ? 'Remove bookmark' : 'Bookmark lesson'}
                  >
                    {bookmarked ? <BookmarkedIcon /> : <BookmarkIcon />}
                  </IconButton>
                </>
              )}
              <IconButton onClick={onClose} sx={{ color: 'white' }}>
                <CloseIcon />
              </IconButton>
            </Box>
          </Box>
        </StyledDialogTitle>

        <DialogContent sx={{ p: 0 }}>
          {loading && renderLoadingState()}
          
          {error && renderErrorState()}
          
          {lessonContent && !loading && (
            <ContentContainer>
              {/* Canvas Status Info */}
              {canvasStatus && (
                <Alert severity="info" sx={{ mb: 3 }}>
                  <Typography variant="body2">
                    <strong>Canvas Status:</strong> {canvasStatus.completed ? 'Completed' : 'Not completed'} • 
                    <strong> Type:</strong> {canvasStatus.type} • 
                    <strong> Requirement:</strong> {canvasStatus.completion_requirement || 'None'}
                  </Typography>
                </Alert>
              )}
              
              {/* Lesson Summary */}
              <SummaryCard elevation={3}>
                <CardContent>
                  <Box display="flex" alignItems="center" mb={2}>
                    <PsychologyIcon sx={{ mr: 1, color: 'primary.main' }} />
                    <Typography variant="h6" fontWeight={600}>
                      Lesson Overview
                    </Typography>
                  </Box>
                  
                  <Typography variant="body1" sx={{ mb: 2, lineHeight: 1.6 }}>
                    {lessonContent.summary}
                  </Typography>
                  
                  <Box display="flex" flexWrap="wrap" gap={1}>
                    <MetadataChip variant="time">
                      <ScheduleIcon sx={{ fontSize: '14px' }} />
                      {lessonContent.estimated_time || '5-10 minutes'}
                    </MetadataChip>
                    <MetadataChip variant="type">
                      <AssignmentIcon sx={{ fontSize: '14px' }} />
                      {lessonContent.type || 'Lesson'}
                    </MetadataChip>
                    {demoLessonNumber && (
                      <MetadataChip variant="default">
                        Demo Content
                      </MetadataChip>
                    )}
                  </Box>
                </CardContent>
              </SummaryCard>

              {/* Learning Objectives */}
              {lessonContent.learning_objectives && lessonContent.learning_objectives.length > 0 && (
                <Accordion defaultExpanded sx={{ mb: 3, backgroundColor: 'rgba(255, 255, 255, 0.8)' }}>
                  <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                    <Box display="flex" alignItems="center">
                      <LightbulbIcon sx={{ mr: 1, color: 'warning.main' }} />
                      <Typography variant="h6" fontWeight={600}>
                        Learning Objectives
                      </Typography>
                    </Box>
                  </AccordionSummary>
                  <AccordionDetails>
                    <ObjectivesList>
                      {lessonContent.learning_objectives.map((objective, index) => (
                        <ListItem key={index}>
                          <ListItemIcon>
                            <CheckCircleIcon color="success" />
                          </ListItemIcon>
                          <ListItemText 
                            primary={objective}
                            primaryTypographyProps={{ fontWeight: 500 }}
                          />
                        </ListItem>
                      ))}
                    </ObjectivesList>
                  </AccordionDetails>
                </Accordion>
              )}

              {/* Lesson Sections */}
              {lessonContent.sections && lessonContent.sections.length > 0 && (
                <Box mb={3}>
                  <Typography variant="h6" fontWeight={600} sx={{ mb: 2, display: 'flex', alignItems: 'center' }}>
                    <SchoolIcon sx={{ mr: 1, color: 'primary.main' }} />
                    Lesson Content
                  </Typography>
                  {lessonContent.sections.map((section, index) => renderSection(section, index))}
                </Box>
              )}

              {/* Key Points */}
              {lessonContent.key_points && lessonContent.key_points.length > 0 && (
                <SummaryCard elevation={2} sx={{ mb: 3 }}>
                  <CardContent>
                    <Typography variant="h6" fontWeight={600} sx={{ mb: 2, display: 'flex', alignItems: 'center' }}>
                      <LightbulbIcon sx={{ mr: 1, color: 'warning.main' }} />
                      Key Takeaways
                    </Typography>
                    <Box component="ul" sx={{ pl: 2, mb: 0 }}>
                      {lessonContent.key_points.map((point, index) => (
                        <Typography component="li" key={index} variant="body1" sx={{ mb: 1 }}>
                          {point}
                        </Typography>
                      ))}
                    </Box>
                  </CardContent>
                </SummaryCard>
              )}

              {/* Resources */}
              {lessonContent.resources && lessonContent.resources.length > 0 && (
                <Box>
                  <Typography variant="h6" fontWeight={600} sx={{ mb: 2, display: 'flex', alignItems: 'center' }}>
                    <LinkIcon sx={{ mr: 1, color: 'info.main' }} />
                    Additional Resources
                  </Typography>
                  {lessonContent.resources.map((resource, index) => renderResource(resource, index))}
                </Box>
              )}
            </ContentContainer>
          )}
        </DialogContent>

        <DialogActions sx={{ p: 3, backgroundColor: 'rgba(255, 255, 255, 0.9)' }}>
          <Button onClick={onClose} variant="outlined">
            Close
          </Button>
          {lessonContent && !completed && (
            <Button 
              onClick={handleMarkAsDone}
              variant="contained"
              startIcon={actionLoading === 'done' ? <CircularProgress size={16} /> : <MarkDoneIcon />}
              disabled={actionLoading === 'done' || demoLessonNumber}
              color="success"
            >
              {actionLoading === 'done' ? 'Marking Done...' : 'Mark as Done'}
            </Button>
          )}
        </DialogActions>
      </StyledDialog>

      {/* Notification Snackbar */}
      {notification.open && (
        <Alert 
          severity={notification.severity}
          sx={{ 
            position: 'fixed',
            bottom: 16,
            right: 16,
            zIndex: 2000,
            minWidth: 250
          }}
          onClose={() => setNotification({ open: false, message: '', severity: 'info' })}
        >
          {notification.message}
        </Alert>
      )}
    </>
  );
};

export default LessonViewer; 