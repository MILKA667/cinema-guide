import React, { useEffect, useState } from "react";
import "./Main.css";
import FilmBox from "../FilmBox";
const Main = () => {
  const [recommend_movies, setReccomendMovies] = useState([]);
  const [all_movies, setAllMovies] = useState([]);
  useEffect(() => {
    fetch("http://localhost:5000/api/recomendation")
      .then((res) => res.json())
      .then((data) => setReccomendMovies(data))
      .catch((err) => console.log(err));
  }, []);
  
  useEffect(() => {
    fetch("http://localhost:5000/api/movies")
      .then((res) => res.json())
      .then((data) => setAllMovies(data))
      .catch((err) => console.log(err));
  }, []);

  return (
    <div className="main-inf">
      <div className="recomendation-container">
        <FilmBox Header={1} />
        {recommend_movies.map((movie) => (
          <FilmBox
            key={movie.id}
            title={movie.title}
            poster={movie.poster_url}
          />
        ))}
      </div>
      <div className="main-container">
        <FilmBox Header={2} />
        {all_movies.map((movie) => (
          <FilmBox
            key={movie.id}
            movieId={movie.id}
            title={movie.title}
            poster={movie.poster_url}
          />
        ))}
      </div>
    </div>
  );
};

export default Main;
