import React, { useMemo } from 'react';
import {
  Box,
  Typography,
  Paper,
  Grid,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  LinearProgress,
  Avatar
} from '@mui/material';
import { styled } from '@mui/material/styles';
import {
  TrendingUp as TrendingUpIcon,
  Assessment as AssessmentIcon,
  School as SchoolIcon,
  CheckCircle as CheckCircleIcon,
  Schedule as ScheduleIcon,
  ExpandMore as ExpandMoreIcon,
  PieChart as PieChartIcon,
  Assignment as AssignmentIcon,
  CalendarToday as CalendarIcon
} from '@mui/icons-material';

const StatsContainer = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(3),
  marginBottom: theme.spacing(2),
  borderRadius: theme.spacing(2),
  background: 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)',
  backdropFilter: 'blur(10px)',
}));

const SimpleTag = styled(Box)(({ theme, bgcolor = '#e0e0e0', color = '#333' }) => ({
  display: 'inline-block',
  padding: theme.spacing(0.5, 1),
  borderRadius: theme.spacing(1),
  backgroundColor: bgcolor,
  color: color,
  fontSize: '0.75rem',
  fontWeight: 500,
  margin: theme.spacing(0.25),
}));

const StatCard = styled(Box)(({ theme }) => ({
  height: '100%',
  borderRadius: theme.spacing(2),
  background: 'rgba(255, 255, 255, 0.9)',
  backdropFilter: 'blur(5px)',
  transition: 'all 0.3s ease-in-out',
  '&:hover': {
    transform: 'translateY(-2px)',
    boxShadow: theme.shadows[8],
  },
}));

const StatNumber = styled(Typography)(({ theme }) => ({
  fontSize: '2.5rem',
  fontWeight: 700,
  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
  backgroundClip: 'text',
  WebkitBackgroundClip: 'text',
  WebkitTextFillColor: 'transparent',
  lineHeight: 1,
}));

const ProgressCard = styled(Box)(({ theme }) => ({
  padding: theme.spacing(2),
  borderRadius: theme.spacing(1),
  backgroundColor: 'rgba(255, 255, 255, 0.8)',
  marginBottom: theme.spacing(1),
}));

const SubjectAvatar = styled(Avatar)(({ theme, color }) => ({
  backgroundColor: color,
  width: 40,
  height: 40,
  fontSize: '0.9rem',
  fontWeight: 'bold',
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

const BoardStatistics = ({ boardData, filteredBoardData, weekPlan }) => {
  // Calculate comprehensive statistics
  const stats = useMemo(() => {
    const allCards = Object.values(boardData).flat();
    const filteredCards = Object.values(filteredBoardData).flat();
    
    const totalCards = allCards.length;
    const filteredCount = filteredCards.length;
    const isFiltered = filteredCount !== totalCards;
    
    // Calculate completed vs not completed (homework column = completed)
    const completedCards = boardData['homework']?.length || 0;
    const activeCards = totalCards - completedCards;
    
      const totalLessons = allCards.length; // Each card is now one lesson
  const completedLessons = (boardData['homework'] || []).length; // Each completed card is one lesson
    
    const overallCompletionRate = totalCards > 0 ? Math.round((completedCards / totalCards) * 100) : 0;
    
    // Subject breakdown
    const subjectStats = {};
    allCards.forEach(card => {
      if (card.subject) {
        if (!subjectStats[card.subject]) {
          subjectStats[card.subject] = {
            total: 0,
            completed: 0,
            inProgress: 0,
            todo: 0,
            lessons: 0,
            notes: 0,
            scheduledDays: 0
          };
        }
        
        subjectStats[card.subject].total++;
        subjectStats[card.subject].lessons += 1; // Each card is one lesson
        subjectStats[card.subject].notes += card.notes?.length || 0;
        subjectStats[card.subject].scheduledDays += card.days?.length || 0;
        
        switch (card.status) {
          case 'done':
            subjectStats[card.subject].completed++;
            break;
          case 'in-progress':
            subjectStats[card.subject].inProgress++;
            break;
          case 'to-do':
          default:
            subjectStats[card.subject].todo++;
            break;
        }
      }
    });
    
    // Priority subjects (high lesson count or important subjects)
    const prioritySubjects = Object.entries(subjectStats)
      .filter(([subject, data]) => {
        const highPrioritySubjects = ['Math', 'Maths', 'English', 'Science'];
        return highPrioritySubjects.includes(subject) || data.lessons >= 5;
      })
      .map(([subject]) => subject);
    
    // Calculate completion rates
    const lessonCompletionRate = totalLessons > 0 ? Math.round((completedLessons / totalLessons) * 100) : 0;
    
    // Time-based statistics
    const scheduledDays = new Set();
    allCards.forEach(card => {
      if (card.days) {
        card.days.forEach(day => scheduledDays.add(day));
      }
    });
    
    // Notes and attention items
    const cardsWithNotes = allCards.filter(card => card.notes && card.notes.length > 0);
    const totalNotes = allCards.reduce((sum, card) => sum + (card.notes?.length || 0), 0);
    
    return {
      totalCards,
      filteredCount,
      isFiltered,
      completedCards,
      activeCards,
      totalLessons,
      completedLessons,
      overallCompletionRate,
      lessonCompletionRate,
      subjectStats,
      prioritySubjects,
      scheduledDaysCount: scheduledDays.size,
      cardsWithNotes: cardsWithNotes.length,
      totalNotes,
    };
  }, [boardData, filteredBoardData]);

  const getTopSubjects = () => {
    return Object.entries(stats.subjectStats)
      .sort((a, b) => b[1].lessons - a[1].lessons)
      .slice(0, 5);
  };

  const getMostActiveSubjects = () => {
    return Object.entries(stats.subjectStats)
      .sort((a, b) => b[1].inProgress - a[1].inProgress)
      .slice(0, 3);
  };

  return (
    <StatsContainer elevation={3}>
      <Typography variant="h5" gutterBottom sx={{ 
        display: 'flex', 
        alignItems: 'center', 
        gap: 1,
        fontWeight: 600,
        mb: 3
      }}>
        <TrendingUpIcon />
        Board Analytics
        {stats.isFiltered && (
          <SimpleTag bgcolor="#e0f7fa" color="#00796b">
            Filtered View
          </SimpleTag>
        )}
      </Typography>

      <Grid container spacing={3}>
        {/* Overview Cards */}
        <Grid item xs={12} md={3}>
          <StatCard>
            <Box sx={{ textAlign: 'center', p: 2 }}>
              <SchoolIcon sx={{ fontSize: 40, color: '#667eea', mb: 1 }} />
              <StatNumber>{stats.totalCards}</StatNumber>
              <Typography variant="body2" color="text.secondary">
                Total Subjects
              </Typography>
              {stats.isFiltered && (
                <Typography variant="caption" color="text.primary">
                  ({stats.filteredCount} filtered)
                </Typography>
              )}
            </Box>
          </StatCard>
        </Grid>

        <Grid item xs={12} md={3}>
          <StatCard>
            <Box sx={{ textAlign: 'center', p: 2 }}>
              <AssignmentIcon sx={{ fontSize: 40, color: '#4ECDC4', mb: 1 }} />
              <StatNumber>{stats.totalLessons}</StatNumber>
              <Typography variant="body2" color="text.secondary">
                Total Lessons
              </Typography>
              <Typography variant="caption" color="text.secondary">
                Avg: {Math.round((stats.totalLessons / stats.totalCards) * 10)}/subject
              </Typography>
            </Box>
          </StatCard>
        </Grid>

        <Grid item xs={12} md={3}>
          <StatCard>
            <Box sx={{ textAlign: 'center', p: 2 }}>
              <CheckCircleIcon sx={{ fontSize: 40, color: '#45B7D1', mb: 1 }} />
              <StatNumber>{stats.overallCompletionRate}%</StatNumber>
              <Typography variant="body2" color="text.secondary">
                Completion Rate
              </Typography>
              <Typography variant="caption" color="text.secondary">
                {stats.completedCards}/{stats.totalCards} subjects
              </Typography>
            </Box>
          </StatCard>
        </Grid>

        <Grid item xs={12} md={3}>
          <StatCard>
            <Box sx={{ textAlign: 'center', p: 2 }}>
              <SimpleTag bgcolor="#f39c12" color="white">
                {stats.activeCards}
              </SimpleTag>
              <Typography variant="body2" color="text.secondary">
                Active Learning
              </Typography>
              <Typography variant="caption" color="text.secondary">
                Subjects in Progress
              </Typography>
            </Box>
          </StatCard>
        </Grid>

        {/* Progress Breakdown */}
        <Grid item xs={12} md={6}>
          <StatCard>
            <Box sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <PieChartIcon />
                Progress Overview
              </Typography>
              
              <ProgressCard>
                <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
                  <Typography variant="body2">Completed</Typography>
                  <Typography variant="body2" fontWeight="bold">
                    {stats.completedCards} ({stats.overallCompletionRate}%)
                  </Typography>
                </Box>
                <LinearProgress 
                  variant="determinate" 
                  value={stats.overallCompletionRate}
                  sx={{ 
                    height: 8, 
                    borderRadius: 4,
                    '& .MuiLinearProgress-bar': { backgroundColor: '#45B7D1' }
                  }}
                />
              </ProgressCard>

              <ProgressCard>
                <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
                  <Typography variant="body2">Active Learning</Typography>
                  <Typography variant="body2" fontWeight="bold">
                    {stats.activeCards} ({Math.round((stats.activeCards / stats.totalCards) * 100)}%)
                  </Typography>
                </Box>
                <LinearProgress 
                  variant="determinate" 
                  value={(stats.activeCards / stats.totalCards) * 100}
                  sx={{ 
                    height: 8, 
                    borderRadius: 4,
                    '& .MuiLinearProgress-bar': { backgroundColor: '#4ECDC4' }
                  }}
                />
              </ProgressCard>

              <ProgressCard>
                <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
                  <Typography variant="body2">To Do</Typography>
                  <Typography variant="body2" fontWeight="bold">
                    {stats.totalCards - stats.completedCards - stats.activeCards} ({Math.round(((stats.totalCards - stats.completedCards - stats.activeCards) / stats.totalCards) * 100)}%)
                  </Typography>
                </Box>
                <LinearProgress 
                  variant="determinate" 
                  value={(stats.totalCards - stats.completedCards - stats.activeCards) / stats.totalCards * 100}
                  sx={{ 
                    height: 8, 
                    borderRadius: 4,
                    '& .MuiLinearProgress-bar': { backgroundColor: '#FF6B6B' }
                  }}
                />
              </ProgressCard>
            </Box>
          </StatCard>
        </Grid>

        {/* Subject Breakdown */}
        <Grid item xs={12} md={6}>
          <StatCard>
            <Box sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <PieChartIcon />
                Top Subjects by Lessons
              </Typography>
              
              <List dense>
                {getTopSubjects().map(([subject, data], index) => (
                  <ListItem key={subject} sx={{ px: 0 }}>
                    <ListItemIcon>
                      <SubjectAvatar color={getSubjectColor(subject)}>
                        {subject.charAt(0)}
                      </SubjectAvatar>
                    </ListItemIcon>
                    <ListItemText
                      primary={subject}
                      secondary={`${data.lessons} lessons • ${data.completed}/${data.total} complete`}
                    />
                    <SimpleTag 
                      bgcolor={data.completed === data.total ? '#4CAF50' : '#e0e0e0'}
                      color={data.completed === data.total ? 'white' : 'inherit'}
                    >
                      {Math.round((data.completed / data.total) * 100)}%
                    </SimpleTag>
                  </ListItem>
                ))}
              </List>
            </Box>
          </StatCard>
        </Grid>

        {/* Additional Statistics */}
        <Grid item xs={12}>
          <StatCard>
            <Box sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <CalendarIcon />
                Weekly Insights
              </Typography>
              
              <Grid container spacing={2}>
                <Grid item xs={12} md={3}>
                  <Box textAlign="center" p={2}>
                    <Typography variant="h4" color="primary" fontWeight="bold">
                      {stats.scheduledDaysCount}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Scheduled Days
                    </Typography>
                  </Box>
                </Grid>
                
                <Grid item xs={12} md={3}>
                  <Box textAlign="center" p={2}>
                    <Typography variant="h4" color="warning.main" fontWeight="bold">
                      {stats.cardsWithNotes}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Cards with Notes
                    </Typography>
                  </Box>
                </Grid>
                
                <Grid item xs={12} md={3}>
                  <Box textAlign="center" p={2}>
                    <Typography variant="h4" color="info.main" fontWeight="bold">
                      {stats.prioritySubjects.length}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Priority Subjects
                    </Typography>
                  </Box>
                </Grid>
                
                <Grid item xs={12} md={3}>
                  <Box textAlign="center" p={2}>
                    <Typography variant="h4" color="success.main" fontWeight="bold">
                      {stats.lessonCompletionRate}%
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Lesson Progress
                    </Typography>
                  </Box>
                </Grid>
              </Grid>

              {stats.prioritySubjects.length > 0 && (
                <Box mt={2}>
                  <Typography variant="subtitle2" gutterBottom>
                    Priority Subjects:
                  </Typography>
                  <Box display="flex" flexWrap="wrap" gap={1}>
                    {stats.prioritySubjects.map(subject => (
                      <SimpleTag
                        key={subject}
                        bgcolor={getSubjectColor(subject)}
                        color="white"
                      >
                        {subject}
                      </SimpleTag>
                    ))}
                  </Box>
                </Box>
              )}
            </Box>
          </StatCard>
        </Grid>
      </Grid>
    </StatsContainer>
  );
};

export default BoardStatistics; 