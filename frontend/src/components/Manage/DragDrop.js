import React from 'react';

function DragDrop() {
        //drag state
        const [dragActive, setDragActive] = React.useState(false);
        // want a button for keyboard users, use the useRef hook
        const inputRef = React.useRef(null);

        //handle drag events
        const handleDrag = function(e) {
            e.preventDefault();
            e.stopPropagation();
            if (e.type === "dragenter" || e.type === "dragover") {
                setDragActive(true);
            } else if (e.type === "dragleave") {
                setDragActive(false);
            }
        }

        //this is triggered when a file is dropped
        // this function resets the dragActive state to "false" because you drop liao then the drag action ends.
        // it also checks if at least one file has been dropped so that something can be done with it.
        const handleDrop = function (e) {
            e.preventDefault();
            e.stopPropagation();
            setDragActive(false);
            if (e.dataTransfer.files && e.dataTransfer.files[0]){
                //need to send it back to our server, or some project storage 
            }
        }

        //this is triggered when the upload button is clicked and we select the file manually in true old fashion way.
        const handleChange =function(e){
            e.preventDefault();
            if(e.target.files && e.target.files[0]){
                //need to send it back to our server, or some project storage
            }
        }

        //will trigger input when the button is clicked
        const onButtonClick =() => {
            inputRef.current.click();
        }

        return (
        <form id="form-file-upload" onDragEnter={handleDrag} onSubmit={(e) => e.preventDefault()}>
            <input ref={inputRef} type="file" id="input-file-upload" multiple={true} onChange={handleChange}/>
            <label id="label-file-upload" htmlFor="input-file-upload" className= {dragActive ? "drag-active":""}>
                <div>
                    <p>Drag and drop your file here or</p>
                    <button className="upload-button" onClick={onButtonClick}>Upload a file</button>
                </div>
            </label>
            { dragActive && 
            <div> 
                id="drag-file-element" onDragEnter={handleDrag} onDragLeave={handleDrag} onDragOver={handleDrag} onDrop={handleDrop} 
            </div>}
        </form>
    )
}

export default DragDrop;