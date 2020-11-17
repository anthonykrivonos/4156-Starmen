import Base64 from 'crypto-js/enc-base64'
import Utf8 from 'crypto-js/enc-utf8'

/** Encodes and decodes objects. */
export class Hasher {
	/**
	 * Encodes the provided object.
	 * @param obj The object to decode.
	 * @returns The encoded hash.
	 */
	public static encode = (obj: any): string => {
		return Base64.stringify(Utf8.parse(JSON.stringify(obj)))
	}

	/**
	 * Decodes the hash, returning null if it's invalid.
	 * @param hash The encoded hash.
	 * @returns The original object or null.
	 */
	public static decode = (hash: string): any | null => {
		try {
			return JSON.parse(Utf8.stringify(Base64.parse(hash)))
		} catch (e) {
			return null
		}
	}
}
