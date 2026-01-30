import './App.css';
import { Paper } from '@material-ui/core';
import AddToDo from "./AddBook"
import Axios from "axios"


function App() {
  const add = (book) =>{
    Axios.post("http://127.0.0.1:7000/cqrs/book/", book).then((response) => {
      if(response.data.bid){
        alert("삽입에 성공")
      }else{
        alert("삽입 실패")
      }
    })
  }

  return (
    <div className="App">
      <Paper style={{ margin:16}}>
        
      </Paper>
    </div>
  );
}

export default App;
