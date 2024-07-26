import * as React from 'react';
import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormControl from '@mui/material/FormControl';
import FormLabel from '@mui/material/FormLabel';

export default function ObjectiveList() {
  const [value, setValue] = React.useState('female');

  const handleChange = (event) => {
    setValue(event.target.value);
  };

  return (
    <FormControl>
      <FormLabel id="demo-controlled-radio-buttons-group" style={{color:"white"}}>Objectives</FormLabel>
      <RadioGroup
        row
        aria-labelledby="demo-controlled-radio-buttons-group"
        name="controlled-radio-buttons-group"
        value={value}
        onChange={handleChange}
      >
        <FormControlLabel
          value="Makespan"
          control={<Radio sx={{ color: 'white', '&.Mui-checked': { color: 'white' }, '& .MuiSvgIcon-root': { color: 'white' } }} />}
          label="Minimise Makespan"
          style={{ color: 'white' }}
        />
        <FormControlLabel
          value="Cost"
          control={<Radio sx={{ color: 'white', '&.Mui-checked': { color: 'white' }, '& .MuiSvgIcon-root': { color: 'white' } }} />}
          label="Minimise WIP Holding Costs"
          style={{ color: 'white' }}
        />
        <FormControlLabel
          value="Runtime"
          control={<Radio sx={{ color: 'white', '&.Mui-checked': { color: 'white' }, '& .MuiSvgIcon-root': { color: 'white' } }} />}
          label="Minimise Runtime"
          style={{ color: 'white' }}
        />
        <FormControlLabel
          value="Tardiness"
          control={<Radio sx={{ color: 'white', '&.Mui-checked': { color: 'white' }, '& .MuiSvgIcon-root': { color: 'white' } }} />}
          label="Minimise Number of Tardy Jobs"
          style={{ color: 'white' }}
        />
      </RadioGroup>
    </FormControl>
  );
}