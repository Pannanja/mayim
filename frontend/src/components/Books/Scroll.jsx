import React from 'react';
import './Scroll.css'; // Make sure to create and style this CSS file

const ScrollEndLeft = () => {
    return <div className="scroll-end-left"></div>;
};

const ScrollEndMiddle = () => {
    return <div className="scroll-end-middle"></div>;
};

const ScrollEndRight = () => {
    return <div className="scroll-end-right"></div>;
};

const Scroll = ({ children }) => {
    return (
        <div className="scroll-container">
            <div className="scroll-end-container">
            <ScrollEndLeft />
            <ScrollEndMiddle />
            <ScrollEndRight />
            </div>
            {children}
            <div className="scroll-end-container">
            <ScrollEndLeft />
            <ScrollEndMiddle />
            <ScrollEndRight />
            </div>
        </div>
    );
};

export default Scroll;