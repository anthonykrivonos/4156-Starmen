import React, { Component } from 'react'
import * as t from 'prop-types'

import { colors } from '../../constants'

import styles from './Button.module.sass'

enum ButtonState {
	normal,
	hovered,
	pressed,
}

export class Button extends Component {
	private buttonState!: ButtonState

	public static propTypes = {
		id: t.string,
		text: t.string,
		onClick: t.func,
		iconName: t.string,
		iconColor: t.string,
		iconSize: t.oneOfType([t.number, t.string]),
		activeOpacity: t.number,
		activeMagnify: t.number,
		className: t.string,
		disabled: t.bool,
	}

	public static defaultProps = {
		id: null,
		text: null,
		iconName: null,
		iconColor: colors.white,
		iconSize: '1.6rem',
		activeOpacity: 0.8,
		activeMagnify: 1.05,
		className: '',
		disabled: false,
	}

	constructor(props: any) {
		super(props)
		this.buttonState = ButtonState.normal
		this.state = { opacity: 1, magnify: 1 }
	}

	public render() {
		const { id, text, iconName, className, disabled, iconSize } = this.props as any
		const { opacity, magnify } = this.state as any
		return (
			<span className={'d-inline-block'}>
				<button
					id={id}
					disabled={disabled}
					onMouseDown={disabled ? undefined : this.onMouseDown}
					onMouseUp={disabled ? undefined : this.onMouseUp}
					onMouseEnter={disabled ? undefined : this.onHover}
					onMouseLeave={disabled ? undefined : this.onHoverOut}
					className={`${styles.button_wrapper} d-flex align-items-center justify-content-start animated ${
						disabled ? 'disabled' : ''
					} ${className}`}
					style={{
						opacity,
						transform: `scale(${magnify})`,
					}}
				>
					{iconName && (
						<img
							src={iconName}
							alt={text}
							className={styles.icon}
							style={{ height: iconSize, width: iconSize }}
						/>
					)}
					{text && <div className={'unselectable'}>{text}</div>}
				</button>
			</span>
		)
	}

	public getState = () => this.buttonState

	private onMouseDown = () => {
		this.buttonState = ButtonState.pressed
		const activeOpacity = (this.props as any).activeOpacity
		this.setState({ opacity: activeOpacity })
		const onClick = (this.props as any).onClick
		if (onClick) {
			onClick()
		}
	}

	private onMouseUp = () => {
		this.buttonState = ButtonState.normal
		this.setState({ opacity: 1 })
	}

	private onHover = () => {
		this.buttonState = ButtonState.hovered
		const activeMagnify = (this.props as any).activeMagnify
		this.setState({ magnify: activeMagnify })
	}

	private onHoverOut = () => {
		this.buttonState = ButtonState.normal
		this.setState({ magnify: 1 })
	}
}
