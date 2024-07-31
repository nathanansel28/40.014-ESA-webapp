import * as React from 'react';
import Box from '@mui/material/Box';
import Stepper from '@mui/material/Stepper';
import Step from '@mui/material/Step';
import StepLabel from '@mui/material/StepLabel';
import UploadFile from './UploadFile';
import Objectives from './Objectives';
import { Gantt } from 'gantt-task-react';

const steps = [
  'Prepare Your CSV File',
  'Upload the CSV File',
  'Select a Minimization Objective',
  'Generating Gantt Chart',
];

const stepComponents = [
    <UploadFile/>,
    <UploadFile/>,
    <Objectives/>,
    <Gantt/>,
  ];

  export default function ProgressBar() {
    const [activeStep, setActiveStep] = React.useState(0);
    const sectionRefs = steps.map(() => React.createRef());
  
    React.useEffect(() => {
      const observer = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              const index = sectionRefs.findIndex((ref) => ref.current === entry.target);
              setActiveStep(index);
            }
          });
        },
        { threshold: 0.5 } // Adjust threshold as needed
      );
  
      sectionRefs.forEach((ref) => {
        if (ref.current) {
          observer.observe(ref.current);
        }
      });
  
      return () => {
        sectionRefs.forEach((ref) => {
          if (ref.current) {
            observer.unobserve(ref.current);
          }
        });
      };
    }, [sectionRefs]);
  
    return (
      <div style={{ backgroundColor: 'rgba(0, 0, 0, 0.7)', padding: '10px' }}>
        <Box sx={{ width: '100%', position: 'fixed' }}>
          <Stepper activeStep={activeStep} alternativeLabel>
            {steps.map((label, index) => (
              <Step key={label}>
                <StepLabel
                  sx={{
                    '& .MuiStepLabel-label': {
                      color: 'white',
                    },
                    '& .MuiStepLabel-label.Mui-active': {
                      color: 'white',
                    },
                    '& .MuiStepIcon-root': {
                      color: 'blue', // Change step icon color
                    },
                    '& .MuiStepLabel-label.Mui-completed': {
                      color: 'white',
                    },
                  }}
                >
                  {label}
                </StepLabel>
              </Step>
            ))}
          </Stepper>
        </Box>

      </div>
    );
  }