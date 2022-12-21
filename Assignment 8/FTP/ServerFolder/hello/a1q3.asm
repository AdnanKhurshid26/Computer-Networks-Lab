.MODEL SMALL
.STACK 100H

.DATA
    MSG1 DB "ENTER 1ST NUMBER : $"
    MSG2 DB 0AH,0DH,"ENTER 2ND NUMBER : $"
    MSG3 DB 0AH,0DH,"SUM : $"
    
    A DW ?
    B DW ?
    SUM DW ?
    CARRY DB 00H

.CODE
    MAIN PROC
        MOV AX,@DATA
        MOV DS,AX
    
        ;DISPLAY MSG1
        LEA DX,MSG1
        MOV AH,09H
        INT 21h
        LEA SI,A
        CALL GET8
        MOV [SI+1],AL
        CALL GET8
        MOV [SI],AL
        
        LEA DX,MSG2
        MOV AH,09H
        INT 21h
        LEA SI,B
        CALL GET8
        MOV [SI+1],AL
        CALL GET8
        MOV [SI],AL
        
        MOV AX,A
        ADD AX,B
        JNC SKIP
        INC CARRY
SKIP:   MOV SUM,AX

        MOV AH,09H
        LEA DX,MSG3
        INT 21H
        
        ;CHECK IF CARRY THEN DISPLAY CARRY
        CMP CARRY,00H
        JNE NOCARRY
        MOV DL,CARRY
        ADD DL,30H
        MOV AH,02H
        INT 21h
NOCARRY: LEA SI,SUM
        INC SI
        CALL PUT8
        DEC SI
        CALL PUT8
        
        MOV AH,4CH
        INT 21H

    MAIN ENDP

    GET8 PROC
        PUSH CX
        PUSH DX
        MOV CL,04H
        MOV DL,00H
        ;GET 1ST NUMBER CHARACTER
        MOV AH,01H
        INT 21h
        SUB AL,30H
        CMP AL,09H
        JLE ISNUM1
        SUB AL,07H
ISNUM1: SHL AL,CL
        OR DL,AL

        ;GET 2ND NUMBER CHARACTER
        MOV AH,01H
        INT 21h
        SUB AL,30H
        CMP AL,09H
        JLE ISNUM2
        SUB AL,07H
ISNUM2: OR DL,AL
        MOV AL,DL
        POP DX
        POP CX
        RET
    GET8 ENDP

    PUT8 PROC
        PUSH CX
        MOV AL,[SI]
        AND AL,0F0H
        MOV CL,04H
        ROL AL,CL
        ADD AL,30H
        CMP AL,39H
        JLE P1 
        ADD AL,07H
P1:     MOV AH,02H
        MOV DL,AL
        INT 21H
        
        MOV AL,[SI]
        AND AL,0FH
        ADD AL,30H
        CMP AL,39H
        JLE P2
        ADD AL,07H
P2:     MOV AH,02H
        MOV DL,AL
        INT 21H
        
        POP CX
        RET
    PUT8 ENDP
END MAIN
    
    