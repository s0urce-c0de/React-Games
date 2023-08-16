import Card from './Card.jsx'

export default function cards2data(data) {

  let formatted_data = data.map((obj) => {
    return <Card href={obj.url} title={obj.title} img={obj.image} img-alt={obj.img_alt}/>
  })
  return formatted_data
}