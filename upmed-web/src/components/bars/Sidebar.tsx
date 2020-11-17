import React, { ReactElement } from 'react'

import styles from './Sidebar.module.sass'

import { Patient, HCP } from '../../models'
import { Avatar } from '../../components'

interface SidebarButton {
	text: string
	icon?: ReactElement
	isBottom?: boolean
	centered?: boolean
	active?: boolean
	onClick?: () => void
}

interface SidebarProps {
	buttons: SidebarButton[]
	user?: Patient | HCP
	isPatient: boolean
	className?: string
}

export const Sidebar = (props: SidebarProps) => {
	return (
		<div className={`${styles.sidebar_container} ${props.className}`}>
			<div className={styles.sidebar_inner}>
				{props.user && (
					<div className={styles.user_container}>
						<Avatar user={props.user} size={'80px'} />
						<div className={styles.user_creds}>
							<div>
								{props.user.firstName} {props.user.lastName}
							</div>
							{!props.isPatient && (props.user as HCP).title && (
								<div className="h7 font-weight-bolder">{(props.user as HCP).title}</div>
							)}
							<div className={styles.email}>{props.user.email}</div>
						</div>
						<div className={styles.divider} />
					</div>
				)}
				{props.buttons
					.filter((b) => !b.isBottom)
					.map((button, idx) => (
						<div
							onClick={button.onClick}
							key={`sidebar-btn-top-${idx}`}
							className={`${styles.sidebar_button} clickable unselectable`}
						>
							{button.icon && <div className={'col-3 p-0'}>{button.icon}</div>}
							<div
								className={`p-0 ${button.icon ? 'col-9' : 'col-12'} ${
									button.centered ? 'text-center' : 'text-left'
								} ${button.active ? 'font-weight-bolder color-white' : 'color-light'}`}
							>
								{button.text}
							</div>
						</div>
					))}
			</div>
			<div className={styles.sidebar_bottom}>
				{props.buttons
					.filter((b) => b.isBottom)
					.map((button, idx) => (
						<div
							onClick={button.onClick}
							key={`sidebar-btn-bottom-${idx}`}
							className={`${styles.sidebar_button} ${styles.button_bottom} clickable unselectable`}
						>
							{button.icon && <div className={'col-3'}>{button.icon}</div>}
							<div
								className={`${button.icon ? 'col-9' : 'col-12'} ${
									button.centered ? 'text-center' : 'text-left'
								}`}
							>
								{button.text}
							</div>
						</div>
					))}
				<div className={styles.bottom_container}>
					<div className={styles.divider} />
					<div className={`${styles.logo} logo unselectable`}>upmed</div>
				</div>
			</div>
		</div>
	)
}
