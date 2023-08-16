import './Card.css'

export default function Card(props)  {
  
  return (
    <div className="Card">
      <h4>{props.title}</h4>
      <img src={props.img} alt={props['img-alt']}></img>
      <a href={props.href} target="_blank" rel="noreferrer">Play Now!</a>
    </div>
  )
}