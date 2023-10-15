import Head from 'next/head'
import dynamic from 'next/dynamic'

const DynamicNav = dynamic(() => import('./components/navbar'), {
    loading: () => <p>Loading...</p>,
})

const DynamicFooter = dynamic(() => import('./components/footer').then((footer) => footer), {
    loading: () => <p>Loading...</p>,
})

function Layout({ children,data}) {
    return (
        <>
        <DynamicNav />
        {children}
        <DynamicFooter/>
        </>
    )
}

export default Layout
