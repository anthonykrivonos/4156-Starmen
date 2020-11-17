import React from 'react'
import { Link } from 'react-router-dom'
import { Button } from '../../components'
import { PEOPLE, LAPTOP, SUITCASE, CASH, LANDING, LANDING2 } from '../../assets'
import styles from './Home.module.sass'

export const Home = () => {
	return (
		<main>
			<section id="header" className={styles.header}>
				<div className={styles.intro}>
					<h2>Healthcare in 2020 that doesn't compromise.</h2>
					<p className={styles.subtitle}>Visit world-class clinicians virtually in just a few clicks.</p>
					<Link to="/signin">
						<Button className={styles.upmed_btn} text="Get Started" />
					</Link>
				</div>
				<img className={styles.landing_img} src={LANDING} alt="people coding on laptops" />
			</section>
			<section id="how-it-works" className={styles.how_it_works}>
				<img className={styles.landing_img} src={LANDING2} alt="hands" />
				<div className="instructions">
					<h2 className="font-title">How does it work?</h2>
					<span className={styles.step}>
						<img src={PEOPLE} alt="person icon" />
						<p>
							Sign in with just <b>one click</b> and create your account in a breeze.
						</p>
					</span>
					<span className={styles.step}>
						<img src={SUITCASE} alt="suitcase icon" />
						<p>
							Choose from <b>hundreds</b> of healthcare providers and clinicians.
						</p>
					</span>
					<span className={styles.step}>
						<img src={LAPTOP} alt="laptop icon" />
						<p>
							Create a virtual appointment in a <b>few easy steps</b>.
						</p>
					</span>
					<span className={styles.step}>
						<img src={CASH} alt="cash icon" />
						<p>
							<b>Save money</b> with low-cost virtual checkups.
						</p>
					</span>
				</div>
			</section>
		</main>
	)
}
