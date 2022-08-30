# # bindata = format(4, "b")

# # print(bindata)

# # def extractCount(frame,window):
# #     # start = -1
# #     # end = -1
# #     endpos = 2**(window-1)
# #     # for i in range(len(frame)-1):
# #     #     if frame[i] == '/':
# #     #         if start == -1:
# #     #             start = i+1
# #     #         else:
# #     #             end = i
# #     return frame[-endpos:]
# #     # return int(cnt)

# # print(extractCount(1000101,3))


# def getCount(frame,window):
        
#         b = format(window, "b")

       
#         return  frame[-len(b):]

# s = getCount("1000101",9)
# print(s)


    
bindata = format(1, "b")

print(bindata)