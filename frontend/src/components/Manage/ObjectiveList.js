import React from 'react';
import './Objectives.css'; // Make sure the path is correct

const ObjectiveList = () => {
    return (
        <div className="objective-list-container">
            <label className="objective-option">
                <input type="radio" name="objective" value="Minimise Makespan" />
                Minimise Makespan
            </label>
            <label className="objective-option">
                <input type="radio" name="objective" value="Minimise WIP Holding Costs" />
                Minimise WIP Holding Costs
            </label>
            <label className="objective-option">
                <input type="radio" name="objective" value="Minimise Runtime" />
                Minimise Runtime
            </label>
            <label className="objective-option">
                <input type="radio" name="objective" value="Minimise Tardiness" />
                Minimise Tardiness
            </label>
        </div>
    );
};

<<<<<<< HEAD
export default ObjectiveList;
=======
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
>>>>>>> 71d801f7e3825560f3fba08ffed6c8d7a7681257
