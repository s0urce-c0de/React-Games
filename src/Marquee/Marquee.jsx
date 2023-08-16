import React, { useState } from 'react'
import './Marquee.css'

function flatten(children) {
  return React.Children.map(children, child => {
    if (Array.isArray(child)) {
      return flatten(child);
    }
    return child;
  });
}

export default function Marquee(props) {
  const [hovered, setHovered] = useState(false);
  let flattened_children=flatten(props.children);
  let flattened_children_height=[];
  for (let index=0; index<=flattened_children.length; index++) {
    flattened_children_height.push(flattened_children.height)
  };
  let length=flattened_children.length;
  let content_styles={
    width: `calc(${length}*(10px+var(--gap)))`,
    animation: `scroll ${length*5}s linear infinite`,
    animationPlayState: hovered ? 'paused' : 'running',
  };
  let container_styles={
    width: `${length*100}%`,
  }
  return (
    <div 
      className="marquee" 
      style={container_styles}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
    >
      <div className="marquee__content" style={content_styles}>{flattened_children}</div>
      <div className="marquee__content" aria-hidden="true" style={content_styles}>{flattened_children}</div>
      <div className="marquee__content" aria-hidden="true" style={content_styles}>{flattened_children}</div>
      <div className="marquee__content" aria-hidden="true" style={content_styles}>{flattened_children}</div>
      <div className="marquee__content" aria-hidden="true" style={content_styles}>{flattened_children}</div>
      <div className="marquee__content" aria-hidden="true" style={content_styles}>{flattened_children}</div>
    </div>
  )
}
