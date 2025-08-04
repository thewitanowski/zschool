import React from 'react';
import {
  Box,
  Typography,
  Paper,
  Grid,
  Chip,
  IconButton,
  Tooltip,
  Avatar,
  Divider,
  Button,
  CircularProgress
} from '@mui/material';
import { styled } from '@mui/material/styles';
import {
  Refresh as RefreshIcon,
  Person as PersonIcon,
  CalendarToday as CalendarIcon,
  School as SchoolIcon,
  Assignment as AssignmentIcon,
  Announcement as AnnouncementIcon,
  RestartAlt as ResetIcon,
  Save as SaveIcon,
  CheckCircle as CheckIcon
} from '@mui/icons-material';

const HeaderContainer = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(3),
  marginBottom: theme.spacing(3),
  borderRadius: theme.spacing(2),
  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
  color: 'white',
  position: 'relative',
  overflow: 'hidden',
  '&::before': {
    content: '""',
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    background: 'rgba(255, 255, 255, 0.1)',
    backdropFilter: 'blur(10px)',
  },
}));

const ContentContainer = styled(Box)({
  position: 'relative',
  zIndex: 1,
});

const TitleSection = styled(Box)(({ theme }) => ({
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'space-between',
  marginBottom: theme.spacing(2),
  flexWrap: 'wrap',
  gap: theme.spacing(1),
}));

const WeekTitle = styled(Typography)(({ theme }) => ({
  fontSize: '2rem',
  fontWeight: 700,
  textShadow: '2px 2px 4px rgba(0, 0, 0, 0.3)',
  [theme.breakpoints.down('sm')]: {
    fontSize: '1.5rem',
  },
}));

const InfoGrid = styled(Grid)(({ theme }) => ({
  marginTop: theme.spacing(2),
}));

const InfoCard = styled(Box)(({ theme }) => ({
  display: 'flex',
  alignItems: 'center',
  gap: theme.spacing(1),
  padding: theme.spacing(1.5),
  backgroundColor: 'rgba(255, 255, 255, 0.15)',
  borderRadius: theme.spacing(1),
  backdropFilter: 'blur(5px)',
  minHeight: '80px', // Ensure consistent height across all tiles
  height: '100%', // Fill the grid item height
}));

const ActionButton = styled(IconButton)(({ theme }) => ({
  backgroundColor: 'rgba(255, 255, 255, 0.2)',
  color: 'white',
  '&:hover': {
    backgroundColor: 'rgba(255, 255, 255, 0.3)',
  },
  transition: 'all 0.3s ease-in-out',
  marginLeft: theme.spacing(1),
}));

const RefreshButton = styled(ActionButton)(({ theme }) => ({
  '&:hover': {
    backgroundColor: 'rgba(255, 255, 255, 0.3)',
    transform: 'rotate(180deg)',
  },
}));

const StatsContainer = styled(Box)(({ theme }) => ({
  display: 'flex',
  gap: theme.spacing(2),
  marginTop: theme.spacing(2),
  flexWrap: 'wrap',
}));

// Replace StatChip with StatTag
const StatTag = styled(Box)(({ theme }) => ({
  display: 'inline-flex',
  alignItems: 'center',
  padding: '4px 12px',
  borderRadius: '16px',
  fontSize: '0.75rem',
  fontWeight: 600,
  backgroundColor: theme.palette.primary.main,
  color: 'white',
  marginLeft: theme.spacing(1),
}));

const SaveIndicator = styled(Box)(({ theme }) => ({
  display: 'flex',
  alignItems: 'center',
  gap: theme.spacing(0.5),
  fontSize: '0.85rem',
  opacity: 0.9,
}));

const WeeklyPlanHeader = ({ 
  weekPlan, 
  onRefresh, 
  onClearBoard, 
  onForceRefresh,
  userSession,
  savingState = false,
  userProfile = null,
  boardData = {}
}) => {
  const formatDate = (dateString) => {
    if (!dateString) return '';
    try {
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
    } catch (error) {
      return dateString;
    }
  };

  const getClassConnectInfo = () => {
    if (!weekPlan.class_connect) return null;
    return `${weekPlan.class_connect.start_time} - ${weekPlan.class_connect.description}`;
  };

  const getTotalLessons = () => {
    if (!weekPlan.classwork) return 0;
    return weekPlan.classwork.reduce((total, work) => {
      return total + (work.lessons ? work.lessons.length : 0);
    }, 0);
  };

  // Calculate lesson completion statistics
  const getLessonStats = () => {
    if (!boardData || Object.keys(boardData).length === 0) {
      return { total: getTotalLessons(), done: 0, todo: getTotalLessons() };
    }

    let total = 0, done = 0;
    
    // Count lesson cards across all columns
    Object.values(boardData).forEach(cards => {
      if (Array.isArray(cards)) {
        cards.forEach(card => {
          if (card.type === 'lesson') {
            total++;
            if (card.status === 'done') {
              done++;
            }
          }
        });
      }
    });

    return {
      total,
      done,
      todo: total - done
    };
  };

  // Calculate homework/assignment statistics
  const getHomeworkStats = () => {
    if (!boardData || Object.keys(boardData).length === 0) {
      return { total: weekPlan.assignments?.length || 0, done: 0, todo: weekPlan.assignments?.length || 0 };
    }

    let total = 0, done = 0;
    
    // Count assignment cards (typically in homework column)
    Object.values(boardData).forEach(cards => {
      if (Array.isArray(cards)) {
        cards.forEach(card => {
          if (card.type === 'assignment') {
            total++;
            if (card.status === 'done') {
              done++;
            }
          }
        });
      }
    });

    return {
      total,
      done,
      todo: total - done
    };
  };

  const lessonStats = getLessonStats();
  const homeworkStats = getHomeworkStats();

  return (
    <HeaderContainer elevation={8}>
      <ContentContainer>
        <TitleSection>
          <Box>
            <WeekTitle variant="h1">
              {userProfile ? `Welcome, ${userProfile.first_name}!` : (weekPlan.title || 'Weekly Plan')}
            </WeekTitle>
            {userProfile && weekPlan.title && (
              <Typography variant="h5" sx={{ opacity: 0.8, mt: 0.5, fontWeight: 500 }}>
                {weekPlan.title}
              </Typography>
            )}
            {weekPlan.week_starting && (
              <Typography variant="h6" sx={{ opacity: 0.9, mt: 0.5 }}>
                {!userProfile && weekPlan.title ? weekPlan.title + ' - ' : ''}Starting {formatDate(weekPlan.week_starting)}
              </Typography>
            )}
            
            {/* Save Status Indicator */}
            {userSession && (
              <SaveIndicator sx={{ mt: 1 }}>
                {savingState ? (
                  <>
                    <CircularProgress size={16} color="inherit" />
                    <Typography variant="caption">Saving progress...</Typography>
                  </>
                ) : (
                  <>
                    <CheckIcon sx={{ fontSize: 16 }} />
                    <Typography variant="caption">Progress saved automatically</Typography>
                  </>
                )}
              </SaveIndicator>
            )}
          </Box>
          
          <Box display="flex" alignItems="center">
            {userProfile?.avatar_url && (
              <Avatar src={userProfile.avatar_url} sx={{ width: 40, height: 40, mr: 2 }} />
            )}

            {onClearBoard && userSession && (
              <Tooltip title="Reset board to default state">
                <ActionButton onClick={onClearBoard} size="large">
                  <ResetIcon />
                </ActionButton>
              </Tooltip>
            )}
            
            <Tooltip title="Refresh weekly plan">
              <RefreshButton onClick={onRefresh} size="large">
                <RefreshIcon />
              </RefreshButton>
            </Tooltip>
            
            {onForceRefresh && (
              <Tooltip title="Force refresh & clear saved data (fixes drag issues)">
                <ActionButton onClick={onForceRefresh} size="large" color="warning">
                  <ResetIcon />
                </ActionButton>
              </Tooltip>
            )}
          </Box>
        </TitleSection>

        <InfoGrid container spacing={3}>
          {/* Teacher Information */}
          {weekPlan.teacher && (
            <Grid item xs={12} sm={6} md={3}>
              <InfoCard>
                <Avatar sx={{ bgcolor: 'rgba(255, 255, 255, 0.3)' }}>
                  <PersonIcon />
                </Avatar>
                <Box>
                  <Typography variant="body1" fontWeight={600}>
                    {weekPlan.teacher.name}
                  </Typography>
                  <Typography variant="body2" sx={{ opacity: 0.8 }}>
                    {weekPlan.teacher.role}
                  </Typography>
                </Box>
              </InfoCard>
            </Grid>
          )}

          {/* Class Connect */}
          {weekPlan.class_connect && (
            <Grid item xs={12} sm={6} md={3}>
              <InfoCard>
                <Avatar sx={{ bgcolor: 'rgba(255, 255, 255, 0.3)' }}>
                  <CalendarIcon />
                </Avatar>
                <Box>
                  <Typography variant="body1" fontWeight={600}>
                    Class Connect
                  </Typography>
                  <Typography variant="body2" sx={{ opacity: 0.8 }}>
                    {weekPlan.class_connect.start_time}
                  </Typography>
                </Box>
              </InfoCard>
            </Grid>
          )}

          {/* This Week - with completion stats */}
          <Grid item xs={12} sm={6} md={3}>
            <InfoCard>
              <Avatar sx={{ bgcolor: 'rgba(255, 255, 255, 0.3)' }}>
                <SchoolIcon />
              </Avatar>
              <Box>
                <Typography variant="body1" fontWeight={600}>
                  This Week
                </Typography>
                <Typography variant="body2" sx={{ opacity: 0.8 }}>
                  {weekPlan.classwork?.length || 0} subjects, {lessonStats.total} lessons
                </Typography>
                {lessonStats.total > 0 && (
                  <Typography variant="caption" sx={{ opacity: 0.7, display: 'block' }}>
                    {lessonStats.done} done • {lessonStats.todo} to do
                  </Typography>
                )}
              </Box>
            </InfoCard>
          </Grid>

          {/* Homework - with completion stats */}
          <Grid item xs={12} sm={6} md={3}>
            <InfoCard>
              <Avatar sx={{ bgcolor: 'rgba(255, 255, 255, 0.3)' }}>
                <AssignmentIcon />
              </Avatar>
              <Box>
                <Typography variant="body1" fontWeight={600}>
                  Homework
                </Typography>
                <Typography variant="body2" sx={{ opacity: 0.8 }}>
                  {homeworkStats.total} assignment{homeworkStats.total !== 1 ? 's' : ''}
                </Typography>
                {homeworkStats.total > 0 && (
                  <Typography variant="caption" sx={{ opacity: 0.7, display: 'block' }}>
                    {homeworkStats.done} done • {homeworkStats.todo} to do
                  </Typography>
                )}
              </Box>
            </InfoCard>
          </Grid>
        </InfoGrid>

        {/* Statistics Chips */}
        <StatsContainer>
          <StatTag>
            <SchoolIcon sx={{ fontSize: '14px', mr: 0.5 }} />
            {`${weekPlan.classwork?.length || 0} Subjects`}
          </StatTag>
          <StatTag>
            <AnnouncementIcon sx={{ fontSize: '14px', mr: 0.5 }} />
            {`${weekPlan.announcements?.length || 0} Announcements`}
          </StatTag>
          {lessonStats.total > 0 && (
            <StatTag>
              {`${lessonStats.total} Lessons (${lessonStats.done} Done)`}
            </StatTag>
          )}
          {homeworkStats.total > 0 && (
            <StatTag>
              <AssignmentIcon sx={{ fontSize: '14px', mr: 0.5 }} />
              {`${homeworkStats.total} Assignments (${homeworkStats.done} Done)`}
            </StatTag>
          )}
          {userSession && (
            <StatTag sx={{ backgroundColor: 'rgba(76, 175, 80, 0.7)' }}>
              <SaveIcon sx={{ fontSize: '14px', mr: 0.5 }} />
              Auto-Save Enabled
            </StatTag>
          )}
        </StatsContainer>

        {/* Important Announcements */}
        {weekPlan.announcements && weekPlan.announcements.length > 0 && (
          <Box mt={2}>
            <Typography variant="body2" sx={{ opacity: 0.9, mb: 1 }}>
              📢 Important Updates:
            </Typography>
            <Box display="flex" flexDirection="column" gap={0.5}>
              {weekPlan.announcements.slice(0, 2).map((announcement, index) => (
                <Typography 
                  key={index}
                  variant="body2" 
                  sx={{ 
                    opacity: 0.8,
                    fontSize: '0.85rem',
                    backgroundColor: 'rgba(255, 255, 255, 0.1)',
                    padding: 1,
                    borderRadius: 1,
                  }}
                >
                  • {announcement.message}
                </Typography>
              ))}
            </Box>
          </Box>
        )}

        {/* Session Information */}
        {userSession && (
          <Box mt={2} sx={{ opacity: 0.7 }}>
            <Typography variant="caption">
              Session ID: {userSession.substring(0, 8)}... | Your progress is automatically saved
            </Typography>
          </Box>
        )}
      </ContentContainer>
    </HeaderContainer>
  );
};

export default WeeklyPlanHeader; 