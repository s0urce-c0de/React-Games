import Card from '../Card/Card.jsx'

export default function Create_Cards(data) {

  let formatted_data = data.map((obj) => {
    return <Card url={obj.url} title={obj.title} img={obj.image} img-alt={obj.img_alt}/>
  })
  return formatted_data
}