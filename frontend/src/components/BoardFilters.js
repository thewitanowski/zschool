import React, { useState, useEffect, useMemo } from 'react';
import {
  Box,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Typography,
  IconButton,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  FormGroup,
  FormControlLabel,
  Checkbox,
  Slider,
  Button,
  Paper,
  Divider
} from '@mui/material';
import { styled } from '@mui/material/styles';
import {
  Search as SearchIcon,
  FilterList as FilterIcon,
  Clear as ClearIcon,
  ExpandMore as ExpandMoreIcon,
  Close as CloseIcon
} from '@mui/icons-material';

// Add SimpleTag component
const SimpleTag = styled(Box)(({ theme, bgcolor = '#e0e0e0', color = '#333' }) => ({
  display: 'inline-flex',
  alignItems: 'center',
  gap: '4px',
  padding: '4px 8px',
  borderRadius: '12px',
  fontSize: '0.75rem',
  fontWeight: 500,
  backgroundColor: bgcolor,
  color: color,
  border: '1px solid rgba(0,0,0,0.1)',
  cursor: 'pointer',
  '&:hover': {
    opacity: 0.8,
  },
}));

const FilterContainer = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(2),
  marginBottom: theme.spacing(2),
  borderRadius: theme.spacing(2),
  background: 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)',
  backdropFilter: 'blur(10px)',
}));

const SearchContainer = styled(Box)(({ theme }) => ({
  display: 'flex',
  alignItems: 'center',
  gap: theme.spacing(2),
  marginBottom: theme.spacing(2),
}));

const FilterChipsContainer = styled(Box)(({ theme }) => ({
  display: 'flex',
  flexWrap: 'wrap',
  gap: theme.spacing(1),
  marginTop: theme.spacing(1),
}));

const StatsBadge = styled(Box)(({ theme }) => ({
  '& .MuiBadge-badge': {
    backgroundColor: theme.palette.primary.main,
    color: 'white',
  },
}));

const BoardFilters = ({
  boardData,
  onFilterChange,
  onSearchChange,
  searchTerm,
  activeFilters,
  showAdvanced = false,
  onToggleAdvanced
}) => {
  const [localSearchTerm, setLocalSearchTerm] = useState(searchTerm || '');
  const [selectedSubjects, setSelectedSubjects] = useState(activeFilters?.subjects || []);
  const [selectedStatuses, setSelectedStatuses] = useState(activeFilters?.statuses || []);
  const [showEmptyColumns, setShowEmptyColumns] = useState(activeFilters?.showEmptyColumns ?? true);
  const [sortBy, setSortBy] = useState(activeFilters?.sortBy || 'alphabetical');
  const [lessonCountRange, setLessonCountRange] = useState(activeFilters?.lessonCountRange || [1, 15]);

  // Available filter options
  const availableStatuses = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'homework'];
  const availableSubjects = [...new Set(Object.values(boardData).flat().map(card => card.subject))];
  
  const statistics = useMemo(() => {
    const allCards = Object.values(boardData).flat();
    const filteredCards = Object.values(boardData).flat();
    
    const subjectCounts = {};
    const statusCounts = {
      'monday': boardData['monday']?.length || 0,
      'tuesday': boardData['tuesday']?.length || 0,
      'wednesday': boardData['wednesday']?.length || 0,
      'thursday': boardData['thursday']?.length || 0,
      'friday': boardData['friday']?.length || 0,
      'homework': boardData['homework']?.length || 0
    };

    allCards.forEach(card => {
      if (card.subject) {
        subjectCounts[card.subject] = (subjectCounts[card.subject] || 0) + 1;
      }
    });

    const totalCards = allCards.length;
    const totalLessons = allCards.length; // Each card is now one lesson

    return {
      totalCards,
      totalLessons,
      subjectCounts,
      statusCounts,
      completionRate: totalCards > 0 ? Math.round((statusCounts.done / totalCards) * 100) : 0
    };
  }, [boardData]);

  // Handle search input changes
  const handleSearchChange = (event) => {
    const value = event.target.value;
    setLocalSearchTerm(value);
    onSearchChange(value);
  };

  // Handle subject filter changes
  const handleSubjectChange = (event) => {
    const value = event.target.value;
    setSelectedSubjects(value);
    updateFilters({ subjects: value });
  };

  // Handle status filter changes
  const handleStatusChange = (event) => {
    const value = event.target.value;
    setSelectedStatuses(value);
    updateFilters({ statuses: value });
  };

  // Update filters and notify parent
  const updateFilters = (newFilters) => {
    const updatedFilters = {
      subjects: selectedSubjects,
      statuses: selectedStatuses,
      showEmptyColumns,
      sortBy,
      lessonCountRange,
      ...newFilters
    };
    onFilterChange(updatedFilters);
  };

  // Clear all filters
  const clearAllFilters = () => {
    setLocalSearchTerm('');
    setSelectedSubjects([]);
    setSelectedStatuses([]);
    setShowEmptyColumns(true);
    setSortBy('alphabetical');
    setLessonCountRange([1, 15]);
    onSearchChange('');
    onFilterChange({
      subjects: [],
      statuses: [],
      showEmptyColumns: true,
      sortBy: 'alphabetical',
      lessonCountRange: [1, 15]
    });
  };

  // Check if any filters are active
  const hasActiveFilters = localSearchTerm || 
    selectedSubjects.length > 0 || 
    selectedStatuses.length > 0 || 
    !showEmptyColumns ||
    sortBy !== 'alphabetical' ||
    lessonCountRange[0] !== 1 || 
    lessonCountRange[1] !== 15;

  return (
    <FilterContainer elevation={3}>
      {/* Main Search and Filter Row */}
      <SearchContainer>
        <TextField
          fullWidth
          variant="outlined"
          placeholder="Search lessons, subjects, or topics..."
          value={localSearchTerm}
          onChange={handleSearchChange}
          InputProps={{
            startAdornment: <SearchIcon sx={{ color: 'text.secondary', mr: 1 }} />,
            endAdornment: localSearchTerm && (
              <IconButton onClick={() => handleSearchChange({ target: { value: '' } })}>
                <ClearIcon />
              </IconButton>
            )
          }}
          sx={{
            '& .MuiOutlinedInput-root': {
              backgroundColor: 'rgba(255, 255, 255, 0.8)',
              backdropFilter: 'blur(5px)',
            }
          }}
        />

        <IconButton 
          onClick={onToggleAdvanced}
          color={showAdvanced ? 'primary' : 'default'}
        >
          <StatsBadge badgeContent={hasActiveFilters ? '●' : 0} invisible={!hasActiveFilters}>
            <FilterIcon />
          </StatsBadge>
        </IconButton>

        {hasActiveFilters && (
          <IconButton onClick={clearAllFilters} color="secondary">
            <ClearIcon />
          </IconButton>
        )}
      </SearchContainer>

      {/* Quick Statistics */}
      <Box display="flex" gap={2} flexWrap="wrap" alignItems="center">
        <Typography variant="body2" color="text.secondary">
          <strong>{statistics.totalCards}</strong> subjects • 
          <strong> {statistics.totalLessons}</strong> lessons • 
          <strong> {statistics.completionRate}%</strong> complete
        </Typography>
        
        {Object.entries(statistics.statusCounts).map(([status, count]) => (
          <SimpleTag
            key={status}
            bgcolor={statistics.statusCounts[status] > 0 ? '#4CAF50' : '#E0E0E0'}
            color={statistics.statusCounts[status] > 0 ? 'white' : 'text.secondary'}
          >
            {status.replace('-', ' ')}: {count}
          </SimpleTag>
        ))}
      </Box>

      {/* Advanced Filters Accordion */}
      {showAdvanced && (
        <Accordion sx={{ mt: 2, backgroundColor: 'rgba(255, 255, 255, 0.5)' }}>
          <AccordionSummary expandIcon={<ExpandMoreIcon />}>
            <Typography variant="h6" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <FilterIcon />
              Advanced Filters
            </Typography>
          </AccordionSummary>
          <AccordionDetails>
            <Box display="flex" flexDirection="column" gap={3}>
              
              {/* Subject Filter */}
              <FormControl fullWidth>
                <InputLabel>Filter by Subjects</InputLabel>
                <Select
                  multiple
                  value={selectedSubjects}
                  onChange={handleSubjectChange}
                  renderValue={(selected) => (
                    <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                      {selected.map((value) => (
                        <SimpleTag
                          key={value}
                          bgcolor={statistics.subjectCounts[value] > 0 ? '#4CAF50' : '#E0E0E0'}
                          color={statistics.subjectCounts[value] > 0 ? 'white' : 'text.secondary'}
                        >
                          {value} ({statistics.subjectCounts[value] || 0})
                        </SimpleTag>
                      ))}
                    </Box>
                  )}
                >
                  {availableSubjects.map((subject) => (
                    <MenuItem key={subject} value={subject}>
                      <SimpleTag
                        bgcolor={statistics.subjectCounts[subject] > 0 ? '#4CAF50' : '#E0E0E0'}
                        color={statistics.subjectCounts[subject] > 0 ? 'white' : 'text.secondary'}
                      >
                        {subject} ({statistics.subjectCounts[subject] || 0})
                      </SimpleTag>
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>

              {/* Status Filter */}
              <FormControl fullWidth>
                <InputLabel>Filter by Status</InputLabel>
                <Select
                  multiple
                  value={selectedStatuses}
                  onChange={handleStatusChange}
                  renderValue={(selected) => (
                    <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                      {selected.map((value) => (
                        <SimpleTag
                          key={value} 
                          bgcolor={statistics.statusCounts[value] > 0 ? '#4CAF50' : '#E0E0E0'}
                          color={statistics.statusCounts[value] > 0 ? 'white' : 'text.secondary'}
                        >
                          {value.replace('-', ' ')}
                        </SimpleTag>
                      ))}
                    </Box>
                  )}
                >
                  {availableStatuses.map((status) => (
                    <MenuItem key={status} value={status}>
                      <SimpleTag
                        bgcolor={statistics.statusCounts[status] > 0 ? '#4CAF50' : '#E0E0E0'}
                        color={statistics.statusCounts[status] > 0 ? 'white' : 'text.secondary'}
                      >
                        {status.replace('-', ' ')} ({statistics.statusCounts[status]})
                      </SimpleTag>
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>

              {/* Sorting Options */}
              <FormControl fullWidth>
                <InputLabel>Sort Cards By</InputLabel>
                <Select
                  value={sortBy}
                  onChange={(e) => {
                    setSortBy(e.target.value);
                    updateFilters({ sortBy: e.target.value });
                  }}
                >
                  <MenuItem value="alphabetical">Alphabetical (A-Z)</MenuItem>
                  <MenuItem value="subject">Subject</MenuItem>
                  <MenuItem value="lessonCount">Number of Lessons</MenuItem>
                  <MenuItem value="recent">Recently Added</MenuItem>
                </Select>
              </FormControl>

              {/* Lesson Count Range */}
              <Box>
                <Typography gutterBottom>
                  Filter by Lesson Count: {lessonCountRange[0]} - {lessonCountRange[1]}
                </Typography>
                <Slider
                  value={lessonCountRange}
                  onChange={(event, newValue) => {
                    setLessonCountRange(newValue);
                    updateFilters({ lessonCountRange: newValue });
                  }}
                  valueLabelDisplay="auto"
                  min={1}
                  max={20}
                  marks={[
                    { value: 1, label: '1' },
                    { value: 5, label: '5' },
                    { value: 10, label: '10' },
                    { value: 15, label: '15' },
                    { value: 20, label: '20+' }
                  ]}
                />
              </Box>

              {/* Display Options */}
              <Box>
                <FormControlLabel
                  control={
                    <Checkbox
                      checked={showEmptyColumns}
                      onChange={(e) => {
                        setShowEmptyColumns(e.target.checked);
                        updateFilters({ showEmptyColumns: e.target.checked });
                      }}
                    />
                  }
                  label="Show empty columns"
                />
                <FormControlLabel
                  control={
                    <Checkbox
                      checked={activeFilters.bookmarked || false}
                      onChange={(e) => {
                        updateFilters({ bookmarked: e.target.checked || undefined });
                      }}
                    />
                  }
                  label="📌 Show only bookmarked items"
                />
              </Box>

              {/* Quick Actions */}
              <Box display="flex" gap={2} justifyContent="space-between">
                <Button
                  variant="outlined"
                  startIcon={<ClearIcon />}
                  onClick={clearAllFilters}
                  disabled={!hasActiveFilters}
                >
                  Clear All Filters
                </Button>
                
                <Box display="flex" gap={1}>
                  <Button
                    size="small"
                    onClick={() => handleSubjectChange({ target: { value: availableSubjects } })}
                  >
                    All Subjects
                  </Button>
                  <Button
                    size="small"
                    onClick={() => handleStatusChange({ target: { value: availableStatuses } })}
                  >
                    All Statuses
                  </Button>
                </Box>
              </Box>

            </Box>
          </AccordionDetails>
        </Accordion>
      )}

      {/* Active Filters Display */}
      {hasActiveFilters && (
        <FilterChipsContainer>
          <Typography variant="body2" color="text.secondary" sx={{ mr: 1 }}>
            Active filters:
          </Typography>
          
          {localSearchTerm && (
            <SimpleTag
              bgcolor="primary.main"
              color="white"
            >
              Search: "{localSearchTerm}"
            </SimpleTag>
          )}
          
          {selectedSubjects.map((subject) => (
            <SimpleTag
              key={subject}
              bgcolor="secondary.main"
              color="white"
            >
              Subject: {subject}
            </SimpleTag>
          ))}
          
          {selectedStatuses.map((status) => (
            <SimpleTag
              key={status}
              bgcolor="info.main"
              color="white"
            >
              Status: {status.replace('-', ' ')}
            </SimpleTag>
          ))}
          
          {sortBy !== 'alphabetical' && (
            <SimpleTag
              bgcolor="default.main"
              color="white"
            >
              Sort: {sortBy}
            </SimpleTag>
          )}
        </FilterChipsContainer>
      )}
    </FilterContainer>
  );
};

export default BoardFilters; 