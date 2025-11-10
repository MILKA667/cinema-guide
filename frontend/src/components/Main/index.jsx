import React, { useEffect, useState } from "react";
import "./Main.css";
import FilmBox from "../FilmBox";
const Main = () => {
  const [movies, setMovies] = useState([]);

  useEffect(() => {
    fetch("http://localhost:5000/api/recomendation")
      .then((res) => res.json())
      .then((data) => setMovies(data))
      .catch((err) => console.log(err));
  }, []);

  return (
    <div className="main-inf">
      <div className="main-container">
        <FilmBox isHeader />
        {movies.map((movie) => (
          <FilmBox
            key={movie.id}
            title={movie.title}
            poster={movie.poster_url}
          />
        ))}
      </div>
    </div>
  );
};

export default Main;
