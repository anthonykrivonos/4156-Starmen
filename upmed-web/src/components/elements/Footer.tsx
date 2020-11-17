import React from 'react'
import { Link } from 'react-router-dom'
import styles from './Footer.module.sass'

export const Footer = () => {
	return (
		<footer id="footer" className={styles.footer}>
			<div className={styles.footer_body}>
				<div className={styles.footer_top}>
					<h2 className={'logo'}>upmed</h2>
					<div className={styles.profiles}>
						<h3>Profile</h3>
						<Link to="/signin">Sign In</Link>
					</div>
					<p className={styles.tagline}>Healthcare, the smarter way</p>
				</div>
				<div className={styles.footer_bottom}>
					<hr />
					<div className={styles.bottom_line}>
						<p>Created for COMS W4156 at Columbia University.</p>
					</div>
				</div>
			</div>
		</footer>
	)
}
