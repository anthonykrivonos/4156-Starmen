import React, { ReactElement, useEffect, useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import './NavigationBar.sass'
import './Hamburgers.css'

interface NavigationItem {
	title: string
	url: string
}

interface NavigationBarProps {
	homeRef?: string
	items?: (NavigationItem | ReactElement)[]
	onResize?: (width: number, height: number) => void
}

export const NavigationBar = (props: NavigationBarProps) => {
	const location = useLocation()

	const [pathname, setPathname] = useState('')
	const [navbarHeight, setNavbarHeight] = useState(0)
	const [isNavBarCollapsed, setIsNavBarCollapsed] = useState(false)
	const [isNavBarSmall, setIsNavBarSmall] = useState(false)
	const [isNavBarTiny, setIsNavBarTiny] = useState(false)

	const toggleNavBar = (show: boolean = isNavBarCollapsed) => setIsNavBarCollapsed(!show)

	const onNavbarResize = (navbar: any) => {
		if (navbar) {
			const navbarRect = navbar.getBoundingClientRect()
			if (!navbarHeight || navbarHeight !== navbarRect.height) {
				setNavbarHeight(navbarRect.height)
				onResize(navbarRect.width, navbarRect.height)
				props.onResize && props.onResize(navbarRect.width, navbarRect.height)
			}
		}
	}

	const onResize = (width: number, height: number) => {
		const RESIZE_THRESH = 992
		const navBarSmall = width < RESIZE_THRESH
		const navBarTiny = window.innerWidth < 580
		if (isNavBarSmall !== navBarSmall && navBarTiny !== isNavBarTiny) {
			setIsNavBarSmall(navBarSmall)
			setIsNavBarTiny(navBarTiny)
		} else if (navBarSmall !== isNavBarSmall) {
			setIsNavBarSmall(isNavBarSmall)
		} else if (navBarTiny !== isNavBarTiny) {
			setIsNavBarTiny(isNavBarTiny)
		}
	}

	useEffect(() => {
		onResize(window.innerWidth, window.innerHeight)
		window.addEventListener('resize', () => {
			onResize(window.innerWidth, window.innerHeight)
		})
	})

	useEffect(() => {
		setPathname(location.pathname)
	}, [location.pathname])

	const navigationItems = props.items || []

	return (
		<nav ref={(r) => onNavbarResize(r)} className={'navbar-wrapper'}>
			<div className="navbar navbar-expand-lg">
				<a className={`${isNavBarSmall ? 'text-center' : 'text-left'} pt-2 pb-2`} href={props.homeRef || '/'}>
					<h3 className={'logo'}>upmed</h3>
				</a>
				<button
					onMouseDown={() => toggleNavBar()}
					className={`navbar-toggler hamburger ${isNavBarCollapsed ? '' : 'is-active'}`}
					type="button"
					data-toggle="collapse"
					data-target=".navbar-collapse"
					aria-controls="navbarText"
					aria-label="toggleNavBar"
				>
					<div className={`hamburger hamburger--minus  ${isNavBarCollapsed ? '' : 'is-active'}`}>
						<div className="hamburger-box">
							<div className="hamburger-inner"></div>
						</div>
					</div>
				</button>
				<div className="collapse navbar-collapse">
					<ul className="navbar-nav ml-auto" id="menu">
						{navigationItems.map((item: NavigationItem | ReactElement, idx: number) => (
							<li key={`nb-${idx}`} className="nav-item" data-menuanchor="Home">
								{item && (item as any).title && (item as any).url ? (
									<div className={'nav-inner'}>
										<Link className="nav-link" to={(item as any).url}>
											{(item as any).title}
										</Link>
										{(item as any).url === pathname && <div className={'ref-underline'}></div>}
									</div>
								) : (
									item
								)}
							</li>
						))}
					</ul>
				</div>
			</div>
		</nav>
	)
}
