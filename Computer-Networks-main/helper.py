#!/usr/bin/env python3

CRCPolynomials = {
    "CRC-8"       : "0b111010101",
    "CRC-10"      : "x^10 + x^9 + x^5 + x^4 + x^1 + 1",
    "CRC-16"      : "x^16 + x^15 + x^2 + 1",
	"CRC-32"      : "x^32 + x^26 + x^23 + x^22 + x^16 + x^12 + x^11 + x^10 + x^8 + x^7 + x^5 + x^4 + x^2 + 1"  
}

def convToBinary(key):
	polynomial = CRCPolynomials[key]
	return polynomial[2:]
	
	