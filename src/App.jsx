// import React from 'react'
import Title from './Title/Title.jsx'
import Path from './Path.jsx'
import Create_Cards from './Create_Cards/Create_Cards.jsx'
import Marquee from './Marquee/Marquee.jsx'
import './App.css'

const my_games = [
  {
    title: 'Hangman',
    image: `${Path}/game-icons/Hangman.png`,
    url: "https://github.com/s0urce-c0de/React-Games/tree/main/games/Hangman/",
    img_alt: "Image not found"
  },
  {
    title: 'Spaceship Game',
    image: `${Path}/game-icons/SpaceShip 2-Player.png`,
    url: "https://github.com/s0urce-c0de/React-Games/tree/main/games/SpaceShip 2-Player/",
    img_alt: "Image not found"
  },
  {
    title: 'Space Invaders',
    image: `${Path}/game-icons/Space Invaders.png`,
    url: "https://github.com/s0urce-c0de/React-Games/tree/main/games/Space Invaders/",
    img_alt: "Image not found"
  }
]

var cards=Create_Cards(my_games);

export default function App(props) {
  
  return (
    <div id="App">
      <Title>Welcome to my games website!</Title>      
      <Marquee>
        {cards}
      </Marquee>
    </div>
  )
}
