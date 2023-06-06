import Title from './Title/Title.jsx'
import Card from './Card/Card.jsx'
import Create_Cards from './Create_Cards/Create_Cards.jsx'
import Marquee from './Marquee/Marquee.jsx'
import React from 'react'
import './App.css'

const my_games = [
  {
    title: 'Spaceship Game',
    image: '/favicon.svg',
    url: "#",
    img_alt: "Image not found"
  },
  {
    title: 'SVG Clock',
    image: '/favicon.svg',
    url: "#",
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
        <Card title="Spaceship Game" img="/favicon.svg" href='https://replit.com/@KanavGupta7/SpaceShip-Game?v=1' img-alt=""/>
        <Card title="Spaceship Game" img="/favicon.svg" href='https://replit.com/@KanavGupta7/SpaceShip-Game?v=1' img-alt=""/>
      </Marquee>
    </div>
  )
}
