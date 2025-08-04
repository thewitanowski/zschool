import React from 'react';
import { Droppable } from '@hello-pangea/dnd';
import {
  Box,
  Typography,
  Paper,
} from '@mui/material';
import { styled } from '@mui/material/styles';
import LessonCard from './LessonCard';

const StyledColumn = styled('div')(({ theme, color }) => ({
  minWidth: '350px',
  maxWidth: '350px',
  margin: '0 10px',
  border: `2px solid ${color}`,
  // Enhanced styling with curved corners and subtle shadow
  borderRadius: theme.spacing(2), // Curved corners
  boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)', // Subtle shadow
  backgroundColor: theme.palette.background.paper, // Clean background
  overflow: 'hidden', // Keep content within rounded corners
  transition: 'transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out', // Smooth transitions
  '&:hover': {
    transform: 'translateY(-2px)', // Subtle lift on hover
    boxShadow: '0 6px 20px rgba(0, 0, 0, 0.15)', // Enhanced shadow on hover
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
  justifyContent: 'center',
  minWidth: '24px',
  height: '20px',
  padding: '0 8px',
  borderRadius: '10px',
  fontSize: '0.75rem',
  fontWeight: 600,
  backgroundColor: theme.palette.primary.main,
  color: 'white',
}));

const DroppableArea = styled('div')(({ theme, isDraggingOver, color }) => ({
  minHeight: '500px',
  padding: '12px',
  borderRadius: theme.spacing(1.5), // Slightly rounded to match column style
  margin: theme.spacing(0.5), // Small margin from column edges
  backgroundColor: isDraggingOver ? `${color}08` : 'transparent', // Subtle highlight when dragging
  transition: 'background-color 0.2s ease-in-out', // Smooth transition
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

const KanbanColumn = ({ columnId, title, color, cards, totalCardCount, onViewLesson, hidden = false }) => {
  return (
    <StyledColumn 
      color={color}
      style={{ display: hidden ? 'none' : 'block' }}
    >
      <ColumnHeader color={color}>
        <ColumnTitle color={color}>
          {title.split(' (')[0]}
        </ColumnTitle>
        <CardCount>
          {cards.length} / {totalCardCount}
        </CardCount>
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
              cards.map((card, index) => {
                // Only log if there's a potential issue
                if (!card.id || index < 0) {
                  console.error(`🚨 Issue with card in ${columnId}:`, {
                    cardId: card.id,
                    index: index,
                    subject: card.subject
                  });
                }
                return (
                  <LessonCard 
                    key={card.id}
                    card={card}
                    index={index}
                    columnId={columnId}
                    onViewLesson={onViewLesson}
                  />
                );
              })
            )}
            {provided.placeholder}
          </DroppableArea>
        )}
      </Droppable>
    </StyledColumn>
  );
};

export default KanbanColumn; 