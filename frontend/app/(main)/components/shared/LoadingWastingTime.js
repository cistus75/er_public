"use client"

import React, { useState, useEffect } from 'react';
import styles from './LoadingWastingTime.module.css'

export default function LoadingWastingTime({message}) {
    const [tmi, setTmi] = useState('');
    const [effect, setEffect] = useState(0);

    useEffect(() => {
        fetch('/loading/tmi.json')
            .then(response => {
                if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
                return response.json();
            })
            .then(data => {
                const randomIndex = Math.floor(Math.random() * data.message.length);
                const randomItem = data.message[randomIndex];
                // console.log(`데이터 길이 : ${data.length}`);
                // console.log(`인덱스 : ${randomIndex}`);
                // console.log(randomItem);
                setTmi(randomItem);
            })
            .catch(error => console.error('Error fetching tmi:', error));
        setEffect(Math.floor(Math.random()*3));
    }, [])

    return (
        <div className={styles.loadingContent}>
            <p className={styles.loadingTitle}>{message}</p>
            {tmi && <p className={`${styles.loadingTmi} ${effect == 0 ? styles.bold :
                    effect == 1 ? styles.italic : styles.underline
                }`}>
                {tmi}
            </p>}
        </div>
    );
} 