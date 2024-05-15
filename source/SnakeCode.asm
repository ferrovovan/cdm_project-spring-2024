			asect 0xF0 # A memory cell used to send instructions
	readyFlags: 	   # to the processor from external circuitry
	
			asect 0xF1 # A memory cell used to exchange segments 
	parts:			   # between the processor and external circuitry
	
			asect 0xF2 # Pointer to the beginning of the queue
	begQueue:
			asect 0xF3 # Pointer to the end of the queue
	endQueue:
			asect 0xF4 # Memory cell storing the queue size
	sizeQueue:		
			asect 0x00
	main:				
			ldi r0, readyFlags
			ld r0, r1
			
			if # Game status check{
				tst r1
			is pl
				# Initialization of variables{ 
				ldi r0, 0x00
				ldi r1, begQueue
				st r1, r0				
				
				ld r1, r1
				ldi r0, 0x04
				st r1, r0
				
				ldi r1, endQueue
				ldi r0, 0x01		
				st r1, r0
				
				ldi r1, sizeQueue
				ldi r0, 1
				st r1, r0 #}
				
				# Waiting for the game to start
				ldi r0, readyFlags
				do	
					ld r0, r1
					tst r1
				until mi
			fi
			#}
			
			
			
			if # Checking for a request to save a new segment to the queue
				shl r1
				tst r1
			is mi
				ldi r2, parts
				ld r2, r2
				move r2, r3
				if # If the segment length is zero, we do not save it
					shl r3
					shl r3
					tst r3
				is nz
					# Saving a new segment and incrementing the queue size {
					ldi r0, endQueue
					ld r0, r0
					st r0, r2
					
					inc r0
					ldi r2, endQueue
					st r2, r0
						
					inc r2
					ld r2, r0
					inc r0
					st r2, r0 #}
					
					# Memory end check and pointer move to beginning (0x00){
					ldi r0, endQueue
					ld r0, r0
					ldi r2, 0xF0
					
					if
						cmp r0, r2
					is eq
						ldi r2, 0x00
						ldi r0, endQueue
						st r0, r2
					fi
					#}
				fi
			fi
			
			
			
			if # Checking for the request to issue the next segment in line to the tail
				shl r1
				tst r1
			is mi
				if # If the queue is not empty, unload the segment and decrement the queue size 
					ldi r0, sizeQueue
					ld r0, r0
					tst r0
				is nz
					dec r0
					ldi r2, sizeQueue
					st r2, r0
					
					ldi r0, begQueue
					ld r0, r0
					ld r0, r0
					ldi r2, parts
					st r2, r0
					
					ldi r0, begQueue
					ld r0, r0
					inc r0
					ldi r2, begQueue
					st r2, r0
					
					# Memory end check and pointer move to beginning (0x00){
					ldi r0, begQueue
					ld r0, r0
					ldi r2, 0xF0
					if
						cmp r0, r2
					is eq
						ldi r2, 0x00
						ldi r0, begQueue
						st r0, r2
					fi
					#}
				fi
			fi				
	br main
	end