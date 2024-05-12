			asect 0xF0
	readyFlags: 
			asect 0xF1
	parts:
			asect 0xF2
	begQueue:
			asect 0xF3
	endQueue:
			asect 0xF4
	sizeQueue:
			asect 0x00
	main:	
			ldi r0, readyFlags	
			ld r0, r1
			if
				tst r1
			is pl
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
				st r1, r0
				
				ldi r0, readyFlags
				do	
					ld r0, r1
					tst r1
				until mi
			fi
			
			
			
			if
				shl r1
				tst r1
			is mi
				ldi r2, parts
				ld r2, r2
				if
					tst r2
				is nz
					ldi r0, endQueue
					ld r0, r0
					st r0, r2
					
					inc r0
					ldi r2, endQueue
					st r2, r0
						
					inc r2
					ld r2, r0
					inc r0
					st r2, r0
						
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
				fi
			fi
			
			
			
			if
				shl r1
				tst r1
			is mi
				if
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
				fi
			fi				
	br main
	end