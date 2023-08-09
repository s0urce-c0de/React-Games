import React, { useState } from 'react'
import './Marquee.css'

function renderChildren(children) {
  return React.Children.map(children, child => {
    if (Array.isArray(child)) {
      return renderChildren(child);
    }
    return child;
  });
}

export default function Marquee(props) {
  const [hovered, setHovered] = useState(false);
  let flattened_children=renderChildren(props.children);
  let length=flattened_children.length;
  let content_styles={
    width: `calc(${length}*(10px+var(--gap)))`,
    animation: `scroll ${length*5}s linear infinite`,
    animationPlayState: hovered ? 'paused' : 'running',
  };
  let container_styles={
    width: `${length*100}%`
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
