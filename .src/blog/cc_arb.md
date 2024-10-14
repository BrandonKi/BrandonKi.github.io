---
title: Credit Card Arbitrage
description: 'Free Money?'
author: Brandon Kirincich
date: 2024-10-13
tags:
  - Finance
  - Arbitrage
---

<!-- https://www.citi.com/credit-cards/citi-custom-cash-credit-card -->

I've been looking into new credit cards, and with the combination of 0% APR introductory periods and bonuses for spending relatively small amounts of money, I saw a low-effort opportunity for arbitrage.

It seems like free money right? So I decided to experiment a bit and see if it's actually worth it.

Here are the terms for the card I was looking at:
- $25K limit
- 0% APR for 15 months
- $200 after spending $1500
- Minimum payment: flat fee or 1%, whichever is higher
- 5% cash back on top spending category, valid for the first $500 spent
- 1% cash back for all other purchases
- No annual fee


## Picking An Investment

First of all, the most important part, is to pick where to put this $25k. This basically comes down to the question, how much risk am I willing to take on?

In this case, my appetite for risk is extremely low, especially since there are some solid risk-free investment options available. I've decided to go with [3 Month Treasury Bills](https://www.investopedia.com/terms/t/treasurybill.asp).[^1]

To somplifiy calcuations, I'll be assuming a flat %5.1 annual return over 15 months(April 2023 to July 2024). Realistically, it's slightly higher, but it won't signifcantly affect the outcome.

![3 Month T Bill Rate](TBillRate.png)

Another option, assuming I was willing to take on some risk, would have been to put the money in [VOO](https://finance.yahoo.com/quote/VOO/) instead, which tracks the S&P 500. Over the same 15-month period, VOO has seen returns of about 33%. Remember though, this involves some added risk, so it's not exactly "free money".

![VOO](voo.png)

## Arbitrage

Ok, now that I've picked where I'll be putting the money, lets see how to maximize returns.

The general strategy is to max out the card and, instead of paying it off, I would instead keep the money in 3 month treasury bills. Also, ideally I would try to maximize rewards and cash back at the same time.

Step one is to max out the card. First of all, since I spent $1,500 I would get $200 right off the bat. Then from the cash back, I would get 5% back on the first $500 and %1 back on the remaining $24,500.[^2] 

This comes out to a total of (0.05 \* $500) + (0.01 \* $24500) + $200 = $470.

Additionally, the interest from 15 months of 3 month treasury bills, assuming a flat 5.1%, is: $25,000 \* 0.051 \* 15/12 = $1,593.75.

That's $1,593.75 + $470 = $2,063.75 in total! It's basically risk-free.

## Minimum Payments

There is one thing I overlooked so far. Even though there's a 15 month 0% APR period, I still need to make the minimum payments. For this card the minimum is 1% per month or a flat fee, whichever is higher. In this case the 1% is definitely higher since we're keeping the card basically maxed out.

Over the course of the whole 15 months, with the help of the finite geometric series formula, I would need to spend ($25,000\*0.01)\*((1-0.99^(15))/(1-0.99))=$3,498.75 on the monthly minimum payments.

In this case, I'll use other income to cover the payments. However, I could also reduce the number of Treasury Bills I purchase by 3 or 4 over the period and apply my cash back rewards toward the payments. If I didn’t use other income, my profit would be around $200 less.

## Conclusion

From this little experiment I would profit $2,063.75, with minimal effort and no risk as well!

If I had a higher risk tolerance I could have invested in VOO instead, which could resulted in a profit of 25000 \* 0.33 \* 15/12 = $10,312.50.

However, this isn’t risk-free, and the safer route still provides an easy profit.

Overall, this can be a way to generate some extra cash with minimal effort, but there are downsides. High credit utilization can negatively impact your credit score, and it also requires a significant amount of available capital upfront. Because of this, there are likely more practical investment options available.

## Notes

[^1]: Just for completeness, it's also possible to get better risk-free returns from CDs or even some HYSAs. I decided to stick with T Bills for this though.

[^2]: You may be thinking that I can actually make a bit more money by simply delaying some of my purchases a single month in order to get 5% cash back. This is true, but the returns would be almost neglible because it would also delay my purchase for another treasury bill. In other words while I would earn more cash back I would also be losing out on interest at the same time.