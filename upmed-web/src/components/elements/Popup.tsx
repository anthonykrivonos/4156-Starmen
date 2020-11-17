import React, { useEffect, useState } from 'react'
import ReactPopup from 'reactjs-popup'

import 'reactjs-popup/dist/index.css'
import styles from './Popup.module.sass'

export interface PopupProps {
	children?: any
	open?: boolean
	autoclose?: boolean
	toggleRef?: (toggler: (toggle: boolean) => void) => void
	onOpen?: () => void
	onClose?: () => void
}

export const Popup = (props: PopupProps) => {
	const [open, setOpen] = useState(props.open !== undefined ? props.open : false)

	useEffect(() => {
		if (props.toggleRef) {
			props.toggleRef((toggle: boolean = true) => {
				setOpen(toggle)
			})
		}
	}, [open, props, props.open])

	const onOpen = () => {
		!open && setOpen(true)
		props.onOpen && props.onOpen()
	}

	const onClose = () => {
		open && setOpen(false)
		props.onClose && props.onClose()
	}

	return (
		<ReactPopup
			position={'center center'}
			open={open}
			closeOnEscape={true}
			closeOnDocumentClick={props.autoclose}
			onOpen={onOpen}
			onClose={onClose}
			overlayStyle={{ transition: '0.3s ease' }}
			contentStyle={{ border: 'none', background: 'none', transition: '0.3s ease' }}
			children={<div className={styles.popup}>{props.children}</div>}
		/>
	)
}
