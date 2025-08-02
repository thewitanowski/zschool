import React from 'react';
import { Droppable } from 'react-beautiful-dnd';
import {
  Box,
  Typography,
  Paper,
} from '@mui/material';
import { styled } from '@mui/material/styles';
import LessonCard from './LessonCard';

const StyledColumn = styled(Paper)(({ theme, color }) => ({
  minWidth: '320px',
  maxWidth: '320px',
  borderRadius: theme.spacing(2),
  padding: theme.spacing(2),
  background: 'rgba(255, 255, 255, 0.1)',
  backdropFilter: 'blur(10px)',
  border: `2px solid ${color}20`,
  borderTop: `4px solid ${color}`,
  boxShadow: theme.shadows[3],
  transition: 'all 0.3s ease-in-out',
  '&:hover': {
    transform: 'translateY(-2px)',
    boxShadow: theme.shadows[6],
    border: `2px solid ${color}40`,
  },
}));

const ColumnHeader = styled(Box)(({ theme, color }) => ({
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'space-between',
  marginBottom: theme.spacing(2),
  padding: theme.spacing(1),
  borderRadius: theme.spacing(1),
  background: `linear-gradient(135deg, ${color}15, ${color}05)`,
}));

const ColumnTitle = styled(Typography)(({ theme, color }) => ({
  fontWeight: 700,
  fontSize: '1.1rem',
  color: color,
  display: 'flex',
  alignItems: 'center',
  gap: theme.spacing(1),
}));

// Replace CardCount Chip with custom Box
const CardCount = styled(Box)(({ theme }) => ({
  display: 'inline-flex',
  alignItems: 'center',
  minWidth: '24px',
  height: '20px',
  padding: '0 8px',
  borderRadius: '10px',
  fontSize: '0.75rem',
  fontWeight: 600,
  backgroundColor: theme.palette.primary.main,
  color: 'white',
  marginLeft: theme.spacing(1),
}));

const DroppableArea = styled(Box, {
  shouldForwardProp: (prop) => prop !== 'isDraggingOver'
})(({ theme, isDraggingOver, color }) => ({
  minHeight: '500px',
  padding: theme.spacing(1),
  borderRadius: theme.spacing(1),
  backgroundColor: isDraggingOver ? `${color}10` : 'transparent',
  border: isDraggingOver ? `2px dashed ${color}60` : '2px dashed transparent',
  transition: 'all 0.3s ease-in-out',
}));

const EmptyState = styled(Box)(({ theme }) => ({
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  justifyContent: 'center',
  height: '200px',
  textAlign: 'center',
  color: theme.palette.text.secondary,
  padding: theme.spacing(2),
}));

const KanbanColumn = ({ columnId, title, color, cards, cardCount, onViewLesson, hidden = false }) => {
  return (
    <StyledColumn 
      elevation={3} 
      color={color}
      style={{ display: hidden ? 'none' : 'block' }}
    >
      <ColumnHeader color={color}>
        <ColumnTitle color={color}>
          {title}
        </ColumnTitle>
        <CardCount label={cardCount} color={color} />
      </ColumnHeader>

      <Droppable droppableId={columnId}>
        {(provided, snapshot) => (
          <DroppableArea
            ref={provided.innerRef}
            {...provided.droppableProps}
            isDraggingOver={snapshot.isDraggingOver}
            color={color}
          >
            {cards.length === 0 ? (
              <EmptyState>
                <Typography variant="body2" sx={{ opacity: 0.7 }}>
                  No items in {title.split(' (')[0].toLowerCase()}
                </Typography>
                <Typography variant="caption" sx={{ opacity: 0.5, mt: 1 }}>
                  Drag cards here to organize your work
                </Typography>
              </EmptyState>
            ) : (
              cards.map((card, index) => (
                <LessonCard 
                  key={card.id}
                  card={card}
                  index={index}
                  columnId={columnId}
                  onViewLesson={onViewLesson}
                />
              ))
            )}
            {provided.placeholder}
          </DroppableArea>
        )}
      </Droppable>
    </StyledColumn>
  );
};

export default KanbanColumn; 