package com.collection;

public class Geek {

	
	/*
	 * public void sound() { System.out.println("ABCD"); }
	 */
	
	String name;
	int id;

	Geek(String name, int id) {
		this.name = name;
		this.id = id;
	}

	@Override
	public int hashCode() {

		return this.id;

		/*
		 * final int prime = 31; int result = 1; result = prime * result + id; result =
		 * prime * result + ((name == null) ? 0 : name.hashCode()); return result;
		 */

	}

	@Override
	public boolean equals(Object obj) {
		if (this == obj)
			return true;
		if (obj == null)
			return false;
		if (getClass() != obj.getClass())
			return false;
		Geek other = (Geek) obj;
		if (id != other.id)
			return false;
		if (name == null) {
			if (other.name != null)
				return false;
		} else if (!name.equals(other.name))
			return false;
		return true;
	}
	 

}
