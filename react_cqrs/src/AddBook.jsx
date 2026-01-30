import React , { useState } from "react"
import { TextField, Paper, Button, Grid } from "@material-ui/core";

function AddToDo(props) {
    const [title, setTitle] = useState("");
    const [author, setAuthor] = useState("");
    const [category, setCategory] = useState("");
    const [pages, setPages] = useState("");
    const [price, setPrice] = useState("");
    const [published_date, setPublished_date] = useState("");
    const [description, setDescription] = useState("");
        const onTitleChange = (event) => {
        setTitle(event.target.value);
    };
    const onAuthorChange = (event) => {
        setAuthor(event.target.value);
    };
    const onCategoryChange = (event) => {
        setCategory(event.target.value);
    };
    const onPagesChange = (event) => {
        setPages(event.target.value);
    };
    const onPriceChange = (event) => {
        setPrice(event.target.value);
    };
    const onPublished_dateChange = (event) => {
        setPublished_date(event.target.value);
    };
    const onDescriptionChange = (event) => {
        setDescription(event.target.value);
    };
    const onSubmit = (event) => {
        event.preventDefault();
        const book = {}
        book.title=title
        book.author = author
        book.category = category
        book.pages = pages
        book.price = price
        book.published_date = published_date
        book.description = description
        props.add(book)
        setTitle("")
        setAuthor("")
        setCategory("")
        setPages("")
        setPrice("")
        setPublished_date("")
        setDescription("")
    };


    return(
        <Paper style={{ margin: 16, padding: 16 }}>
        <Grid container>
          <Grid xs={6} md={6} item style={{ paddingRight: 16 }}>
            <TextField
              onChange={onTitleChange}
              value = {title}
              placeholder="Add Book Title"
              fullWidth
            />
          </Grid>
          <Grid xs={6} md={6} item style={{ paddingRight: 16 }}>
            <TextField
            onChange={onAuthorChange}
            value = {author}
              placeholder="Add Book Author"
              fullWidth
            />
          </Grid>

          <Grid xs={3} md={3} item style={{ paddingRight: 16 }}>
            <TextField
            onChange={onCategoryChange}
            value = {category}
              placeholder="Add Book Category"
              fullWidth
            />
          </Grid>
          <Grid xs={3} md={3} item style={{ paddingRight: 16 }}>
            <TextField
            onChange={onPagesChange}
            value = {pages}
              placeholder="Add Book Pages"
              fullWidth
            />
          </Grid>
          <Grid xs={3} md={3} item style={{ paddingRight: 16 }}>
            <TextField
            onChange={onPriceChange}
            value = {price}
              placeholder="Add Book Price"
              fullWidth
            />
          </Grid>
          <Grid xs={3} md={3} item style={{ paddingRight: 16 }}>
            <TextField
            onChange={onPublished_dateChange}
            value = {published_date}
              placeholder="Add Book Published_Date"
              fullWidth
            />
          </Grid>
          <Grid xs={11} md={11} item style={{ paddingRight: 16 }}>
            <TextField
            onChange={onDescriptionChange}
            value = {description}
              placeholder="Add Book Description"
              fullWidth
            />
          </Grid>
          <Grid xs={1} md={1} item>
            <Button
              fullWidth
              color="secondary"
              variant="outlined"
              onClick={onSubmit}
            >
              +
            </Button>
          </Grid>
        </Grid>
      </Paper>
    );
}

export default AddToDo;

