while True:
    
    st1 = input('Enter the first signature: ')
    st2 = input('Enter the second signature: ')
    if st1 == st2:
        print('The signatures are equals')
    elif st1 == 'e' or st2 == 'e':
        break     
    else:
        print('The signatures are differents')
        
