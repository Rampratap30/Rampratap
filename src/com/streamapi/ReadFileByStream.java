package com.streamapi;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class ReadFileByStream {

	public static void main(String[] args) throws IOException {
		// TODO Auto-generated method stub
		String filePath = "E://test.txt";
		List<String> list = new ArrayList<String>();
		try(Stream<String> stream = Files.lines(Paths.get(filePath))){
			//stream.forEach(System.out::println);
			
			list = stream.filter(line->!line.startsWith("line3")).map(String ::toUpperCase).collect(Collectors.toList());
			
		}
		list.forEach(System.out::println);
	}

}
