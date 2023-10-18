import { NextRequest, NextResponse } from 'next/server'

export function middleware(req: NextRequest) {
    const logger = require("pino")()
//   const nonce = Buffer.from(crypto.randomUUID()).toString('base64')
//   const cspHeader = `
//     default-src 'self';
//     script-src 'self' 'nonce-${nonce}' 'strict-dynamic';
//     style-src 'self' 'nonce-${nonce}';
//     img-src 'self' blob: data:;
//     font-src 'self';
//     object-src 'none';
//     base-uri 'self';
//     form-action 'self';
//     frame-ancestors 'none';
//     block-all-mixed-content;
//     upgrade-insecure-requests;
// `

//   const requestHeaders = new Headers(request.headers)
//   requestHeaders.set('x-nonce', nonce)
//   requestHeaders.set(
//     'Content-Security-Policy',
//     // Replace newline characters and spaces
//     cspHeader.replace(/\s{2,}/g, ' ').trim()
    // )

//   return NextResponse.next({
//     headers: requestHeaders,
//     request: {
//       headers: requestHeaders,
//     },
//   })
  const nonce = `nonce-${Buffer.from(crypto.randomUUID()).toString('base64')}`;
  const isProduction = process.env.NODE_ENV === 'production';
  const devScriptPolicy = ['unsafe-eval']
  const requestHeaders = new Headers(req.headers)
  logger.log(`nonce ${nonce}`)
  requestHeaders.set("nonce", nonce)
  requestHeaders.set('Content-Security-Policy', [
    ['default-src', 'self', nonce],
    ['script-src',  'self', nonce].concat(isProduction ? [] : devScriptPolicy),
    ['connect-src', 'self', nonce],
    ['img-src', 'self', nonce],
    ['style-src', 'self', nonce],
    ['base-uri',  'self', nonce],
    ['form-action', 'self', nonce],
  ].reduce((prev, [directive, ...policy]) => {
    return `${prev}${directive} ${policy.filter(Boolean).map(src => `'${src}'`).join(' ')};`
  }, ''))

//   logger.info(`response headers ${resp.headers}`)
//   return resp
    return NextResponse.next({
        headers: requestHeaders,
        request: {
          headers: requestHeaders,
        },
      })
}

export const config = {
    matcher: [
      /*
       * Match all request paths except for the ones starting with:
       */
      {
        source: '/((?!api|_next|_next/image|favicon.ico).*)',
        missing: [
          { type: 'header', key: 'x-nonce' },
        ],
      },
    ],
  }