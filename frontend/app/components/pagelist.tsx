'use client'

import {
    Pagination,
    PaginationContent,
    PaginationEllipsis,
    PaginationItem,
    PaginationLink,
    PaginationNext,
    PaginationPrevious,
  } from "@/components/ui/pagination"

interface PageListProps {
    totalPages: number;
    page: number,
    setPage:(page:number) => void,
    pageWindowSize: number 
  }
  
export function PageList({ totalPages, page, setPage, pageWindowSize}: PageListProps){
    const getPageNumbers = () => {
      let start
      if (pageWindowSize %2 === 0) {
        start = Math.max(1, page - (pageWindowSize / 2) +1)
      } else {
        start = Math.max(1, page - Math.floor(pageWindowSize / 2))
      }
      
      const end = Math.min(totalPages, start + pageWindowSize - 1)
      if (end - start + 1 < pageWindowSize) {
        start = Math.max(1, end - pageWindowSize + 1)
      }
    
      return Array.from({length: end - start + 1}, (_, i) => start + i)
    }
  
    const handlePageClick = (page: number) => {
      setPage(page);
    };
    
    const handlePrevious = (page: number) => {
      setPage(Math.max(1, page - 1));
    };
    
    const handleNext = (page: number) => {
      setPage(Math.min(totalPages, page + 1));
    };
  
    return (
    <Pagination>
      <PaginationContent >
        {page !== 1 &&(
          <PaginationItem >
            <PaginationPrevious onClick={()=>handlePrevious(page)} />
          </PaginationItem>
        )}
        {getPageNumbers().map(pageNumber => (
          <PaginationItem key={pageNumber} className="cursor-poninter">
            <PaginationLink 
              isActive={page === pageNumber}
              onClick={() => handlePageClick(pageNumber)}
            >
              {pageNumber}
            </PaginationLink>
          </PaginationItem>
        ))}
        {page + Math.floor(pageWindowSize / 2) < totalPages && (
          <PaginationItem>
            <PaginationEllipsis />
          </PaginationItem>
        )}
        {page !== totalPages && (
          <PaginationItem>
            <PaginationNext onClick={()=>handleNext(page)} />
          </PaginationItem>
        )}
      </PaginationContent>
    </Pagination>
    )
  }