import React from 'react'
import ReactLoading from 'react-loading'
import { colors } from '../../constants'

interface LoadingProps {
	text?: string
	type?: 'balls' | 'bars' | 'bubbles' | 'cubes' | 'cylon' | 'spin' | 'spinningBubbles' | 'spokes'
	size?: number | string
	containerClassName?: string
	className?: string
}

export const Loading = (props: LoadingProps) => {
	return (
		<div className={`d-flex flex-column align-items-center justify-content-center ${props.containerClassName}`}>
			{props.text && <div className={'text-center mb-4'}>{props.text}</div>}
			<ReactLoading
				type={props.type || 'spinningBubbles'}
				color={colors.secondary}
				height={props.size ? props.size : '7vw'}
				width={props.size ? props.size : '7vw'}
			/>
		</div>
	)
}
