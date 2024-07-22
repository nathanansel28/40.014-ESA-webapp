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
      <FormLabel id="demo-controlled-radio-buttons-group">Objectives</FormLabel>
      <RadioGroup
        aria-labelledby="demo-controlled-radio-buttons-group"
        name="controlled-radio-buttons-group"
        value={value}gi
        onChange={handleChange}
      >
        <FormControlLabel value="Makespan" control={<Radio />} label="Minimise Makespan" />
        <FormControlLabel value="Cost" control={<Radio />} label="Minimise WIP Holding Costs" />
        <FormControlLabel value="Runtime" control={<Radio />} label="Minimise Runtime" />
        <FormControlLabel value="Tardiness" control={<Radio />} label="Minimise Tardiness" />
      </RadioGroup>
    </FormControl>
  );
}
