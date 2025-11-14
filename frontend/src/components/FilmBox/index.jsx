import React from 'react';
import './style.css';

const FilmBox = ({ Header, title, poster, movieId }) => {

async function watch() {
    const token = localStorage.getItem("token"); 
    if (!token) {
        console.log("No token found");
        return;
    }

    try {
        const res = await fetch("http://localhost:5000/api/watch_movie", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({ movie_id: movieId }) 
        });
        const data = await res.json();
        console.log(data);
    } catch (err) {
        console.error(err);
    }
}


  if (Header == 1) {
    return (
      <div className="film_card header_card">
        <p className="heading">Рекомендации</p>
        <p>На основе ваших интересов</p>
        <p>Cinema-guide</p>
      </div>
    );
  }
  if (Header == 2) {
    return (
      <div className="film_card header_card">
        <p className="heading">Все фильмы</p>
        <p>Нажмите чтобы посмотреть</p>
        <p>Cinema-guide</p>
      </div>
    );
  }


  return (
    <div className="film_card" onClick={watch}>
      <img src={poster} alt={title} className="film_poster" />
      <div className="film_text_overlay">
        <p className="heading">{title}</p>
      </div>
    </div>
  );
};

export default FilmBox;
