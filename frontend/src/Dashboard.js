import React,{useState,useEffect} from "react";
import axios from "axios";


function Dashboard(){


const [tasks,setTasks]=useState([]);

const [title,setTitle]=useState("");

const [description,setDescription]=useState("");



const token=localStorage.getItem("token");



function getTasks(){


axios.get(
"http://127.0.0.1:5000/tasks",
{
headers:{
Authorization:`Bearer ${token}`
}
}

)

.then(res=>{

setTasks(res.data);

});


}



useEffect(()=>{

getTasks();

},[]);





function addTask(){


axios.post(

"http://127.0.0.1:5000/tasks",

{
title,
description
},

{
headers:{
Authorization:`Bearer ${token}`
}
}

)

.then(()=>{

alert("Task Added");

getTasks();

});


}
function updateTask(id){

let status = prompt(
"Enter new status (Pending/Completed)"
);


axios.put(

`http://127.0.0.1:5000/tasks/${id}`,

{
status:status
},

{
headers:{
Authorization:`Bearer ${token}`
}
}

)

.then(()=>{

alert("Task Updated");

getTasks();

});


}




function deleteTask(id){


axios.delete(

`http://127.0.0.1:5000/tasks/${id}`,

{
headers:{
Authorization:`Bearer ${token}`
}
}

)

.then(()=>{

getTasks();

});


}





return(

<div>


<h1>
Task Dashboard
</h1>



<input
placeholder="Task Title"
onChange={
e=>setTitle(e.target.value)
}
/>


<br/>


<textarea

placeholder="Description"

onChange={
e=>setDescription(e.target.value)
}

/>


<br/>


<button onClick={addTask}>
Add Task
</button>



<h2>
My Tasks
</h2>



{

tasks.map(task=>(


<div key={task[0]}>

<h3>
{task[2]}
</h3>


<p>
{task[3]}
</p>


<p>
Status : {task[4]}
</p>


<button

onClick={()=>updateTask(task[0])}

>
Update
</button>


<button

onClick={()=>deleteTask(task[0])}

>
Delete
</button>


</div>


))


}



</div>

)

}


export default Dashboard;
