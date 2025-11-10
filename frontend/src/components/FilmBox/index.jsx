import React from 'react';
import './style.css';

const FilmBox = ({ isHeader, title, poster }) => {
  if (isHeader) {
    return (
      <div className="film_card header_card">
        <p className="heading">Рекомендации</p>
        <p>На основе ваших интересов</p>
        <p>Cinema-guide</p>
      </div>
    );
  }

  return (
    <div className="film_card">
      <img src={poster} alt={title} className="film_poster" />
      <div className="film_text_overlay">
        <p className="heading">{title}</p>
      </div>
    </div>
  );
};

export default FilmBox;
