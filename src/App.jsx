// import React from 'react'
import Title from './Title/Title.jsx'
import Path from './Path.jsx'
import cards2data from './Card/card2data.jsx'
import Marquee from './Marquee/Marquee.jsx'
import './App.css'

const my_games = [
  {
    title: 'Hangman',
    image: `${Path}/game-icons/Hangman.png`,
    url: "https://kanav-g.itch.io/hangman",
    img_alt: "Image not found"
  },
  {
    title: 'Spaceship Game',
    image: `${Path}/game-icons/SpaceShip 2-Player.png`,
    url: "https://kanav-g.itch.io/spaceship-2player",
    img_alt: "Image not found"
  },
  {
    title: 'Space Invaders',
    image: `${Path}/game-icons/Space Invaders.png`,
    url: "https://kanav-g.itch.io/space-invaders",
    img_alt: "Image not found"
  }
]

var cards=cards2data(my_games);

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
